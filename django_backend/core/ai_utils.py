import requests
import json
import re


def analyze_resume_with_ollama(resume_text):
    prompt = f"""
    You are an HR assistant. Please extract the following from this resume:

    1. Full name
    2. Contact info (email, phone)
    3. Skills (as a list)
    4. Latest job title and company
    5. Total years of experience
    6. Education summary
    7. List of keywords

    Resume:
    {resume_text}
    
    Please return a valid JSON object only.
    Do not include Markdown (like ```), no explanations, and no trailing commas.
    Only a pure JSON object with these fields:
    full_name, email, phone, skills (as list), latest_job_title, company, years_experience, education_summary, keywords (as list)
    """

    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        return parse_ollama_json_response(response.json()["response"])
    else:
        return "Error: Could not process resume"


def parse_ollama_json_response(response_text: str):
    try:
        # Remove mark down formatting if exists
        clean_text = response_text.strip()
        clean_text = re.sub(r"^```json", "", clean_text)
        clean_text = re.sub(r"```$", "", clean_text)

        # Trim leading/trailing whitespace or junk
        json_start = clean_text.find("{")
        json_end = clean_text.rfind("}") + 1
        json_str = clean_text[json_start:json_end]

        # Parse safely
        return json.loads(json_str)

    except Exception as e:
        return {"error": f"Failed to parse JSON: {str(e)}"}


def calculate_resume_job_score(resume_text: str, job_description: str):
    prompt = f"""
        You are an AI HR assistant. Your task is to evaluate how well a resume matches a job posting.
    
        Return a compatibility score between 0 and 100 based on how closely the candidate's resume matches the job description. 
        The score should consider experience, skills, and job title relevance.
    
        Return ONLY the following JSON:
        {{
          "score": <integer from 0 to 100>,
          "reason": "<brief explanation why this score was given>"
        }}
    
        Resume:
        \"\"\"
        {resume_text}
        \"\"\"
    
        Job Description:
        \"\"\"
        {job_description}
        \"\"\"
    """
    response = requests.post(
        "http://127.0.0.1:11434/api/generate",
        json={
            "model": "mistral",
            "prompt": prompt,
            "stream": False
        }
    )

    if response.status_code == 200:
        return parse_ollama_json_response(response.json()["response"])
    else:
        return "Error: Could not process resume"
    # try:
    #     # extract JSON from response
    #     start = response.find("{")
    #     end = response.rfind("}") + 1
    #     parsed = json.loads(response[start:end])
    #     return parsed
    # except Exception as e:
    #     return {"score": 0, "reason": "Failed to parse Ollama response"}


if __name__ == '__main__':
    print("Analyzing resume with Ollama...")

    print(analyze_resume_with_ollama(resume_text="ai engineer"))

    print("Finish Analyzing resume with Ollama...")
