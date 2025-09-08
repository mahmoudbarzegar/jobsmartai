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


def parse_ollama_json_response(response_text: any) -> dict:
    try:
        result_text = ""
        if hasattr(response_text, "iter_lines"):
            for line in response_text.iter_lines():
                if line:
                    try:
                        data = json.loads(line)
                        if "response" in data:
                            result_text += data["response"]
                    except json.JSONDecodeError:
                        pass
        else:
            # If not streaming, assume .text or raw string
            result_text = getattr(response_text, "text", str(response_text))

        # Remove mark down formatting if exists
        clean_text = result_text.strip()
        clean_text = re.sub(r"^```json", "", clean_text)
        clean_text = re.sub(r"```$", "", clean_text)

        # Trim leading/trailing whitespace or junk
        json_start = clean_text.find("{")
        json_end = clean_text.rfind("}") + 1

        if json_start != -1 and json_end != -1:
            json_str = clean_text[json_start:json_end]
            try:
                return json.loads(json_str)  # ✅ Return as dict
            except json.JSONDecodeError:
                pass  # Fall back to raw text

            # Step 3: Return plain text if not JSON
        return result_text

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
        return "Error: Could not this process"


def generate_cover_letter(resume_text: str, job_description: str) -> str | dict:
    prompt = f"""
       You are a professional career assistant. Write a concise and tailored cover letter 
       for the following job, using the candidate's resume details.

       Candidate Resume:
       {resume_text}

       Job Description:
       {job_description}

       Instructions:
       - Keep it professional and engaging
       - Highlight matching skills and experience
       - Keep it under 250 words
       - Output only the cover letter text
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
        return parse_ollama_json_response(response)
    else:
        return "Error: Could not this process"


if __name__ == '__main__':
    print("Analyzing resume with Ollama...")
    print(analyze_resume_with_ollama(resume_text="ai engineer"))
    print("Finish Analyzing resume with Ollama...")
