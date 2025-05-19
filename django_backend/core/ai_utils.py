import requests


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
        return response.json()["response"]
    else:
        return "Error: Could not process resume"


if __name__ == '__main__':
    print("Analyzing resume with Ollama...")

    print(analyze_resume_with_ollama(resume_text="ai engineer"))

    print("Finish Analyzing resume with Ollama...")
