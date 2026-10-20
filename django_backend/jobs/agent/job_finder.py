from typing import TypedDict

from langgraph.graph import END, START, StateGraph

from ..models import ApplicationModel, JobModel, ResumeModel
from ..schemas import JobInfo
from ..utils import get_similarity_score, search_job_from_relocate_me, search_jobs_from_remoteok
from ..vector.ollama import analyze_subject_with_ollama, calculate_resume_job_score_description


class FinderState(TypedDict):
    resume_id: int
    skills_left: list[str]
    current_skill: str
    candidates: list[dict]  # new jobs from the latest search
    seen_ids: list[str]  # e.g. "remoteok:12345", so no job is scored twice
    matches: list[dict]
    target: int
    threshold: float
    rounds: int
    max_rounds: int


def pick_skill(state: FinderState):
    skill = state["skills_left"][0]
    return {"current_skill": skill, "skills_left": state["skills_left"][1:]}


def search_jobs(state: FinderState):
    jobs_from_remote_ok = search_jobs_from_remoteok(skills=[state["current_skill"]])
    jobs_from_relocate_me = search_job_from_relocate_me(skills=[state["current_skill"]])
    jobs = jobs_from_remote_ok + jobs_from_relocate_me

    seen = set(state["seen_ids"])
    return {"candidates": [job for job in jobs if job["id"] not in seen]}


def score_jobs(state: FinderState):
    resume = ResumeModel.objects.get(id=state["resume_id"])
    matches = list(state["matches"])
    seen = list(state["seen_ids"])

    for job in state["candidates"]:
        seen.append(job["id"])

        analyze_job_text = analyze_subject_with_ollama(
            subject_text=job["description"], subject_type="job", subject_schema=JobInfo
        )
        data = analyze_job_text.model_dump()

        job_object = JobModel(
            **data,
            title=job["title"],
            description=job["description"],
            link=job["link"],
        )

        score, breakdown = get_similarity_score(job=job_object, resume=resume)

        if score >= state["threshold"]:
            matches.append(
                {
                    "title": job["title"],
                    "link": job["link"],
                    "score": round(score * 100, 1),
                }
            )

            resume_summary = (
                f"{resume.latest_job_title} at {resume.company}, "
                f"{resume.years_experience} years experience. "
                f"Skills: {', '.join(resume.skills)}. {resume.experience_summary}"
            )

            score_description = calculate_resume_job_score_description(
                resume_text=resume_summary, job_description=job_object.description, score=score
            ).reason

            # Save the job FIRST so it gets an id, then link the application to it
            saved_job, _ = JobModel.objects.update_or_create(
                title=job["title"],
                defaults={**data, "description": job["description"], "link": job["link"]},
            )

            application = ApplicationModel(
                resume=resume, job=saved_job, score=score, score_description=score_description
            )
            application.save()

        if len(matches) >= state["target"]:
            break

    return {"matches": matches, "seen_ids": seen, "rounds": state["rounds"] + 1}


def should_continue(state: FinderState):
    if len(state["matches"]) >= state["target"]:
        return "stop"
    if state["rounds"] >= state["max_rounds"] or not state["skills_left"]:
        return "stop"
    return "continue"


graph = StateGraph(FinderState)
graph.add_node("pick_skill", pick_skill)
graph.add_node("search_jobs", search_jobs)
graph.add_node("score_jobs", score_jobs)

graph.add_edge(START, "pick_skill")
graph.add_edge("pick_skill", "search_jobs")
graph.add_edge("search_jobs", "score_jobs")
graph.add_conditional_edges("score_jobs", should_continue, {"continue": "pick_skill", "stop": END})

job_finder = graph.compile()


def find_jobs(resume: ResumeModel, target: int = 10, threshold: float = 0.4) -> list[dict]:
    if not resume.skills:
        return []

    result = job_finder.invoke(
        {
            "resume_id": resume.id,
            "skills_left": list(resume.skills),
            "current_skill": "",
            "candidates": [],
            "seen_ids": [],
            "matches": [],
            "target": target,
            "threshold": threshold,
            "rounds": 0,
            "max_rounds": 8,
        }
    )
    return sorted(result["matches"], key=lambda m: m["score"], reverse=True)
