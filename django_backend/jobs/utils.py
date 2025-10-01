import requests
import fitz

from bs4 import BeautifulSoup


def search_jobs_from_remoteok(skills: list):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/112.0.0.0 Safari/537.36"
        }
        search_keywords = skills[:1]
        query = "+".join(search_keywords)
        url = f"https://remoteok.com/api?tags={query}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return [{"title": job["position"], "link": job["url"], "description": job["description"]}
                    for job in response.json()[1:]]
        return {}
    except Exception as e:
        return {}


def search_job_from_relocate_me(skills: list):
    try:
        search_keywords = skills[:1]
        query = "+".join(search_keywords)
        url = f"https://relocate.me/international-jobs?query={query}"
        headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/112.0.0.0 Safari/537.36"
        }
        result = requests.get(url, headers=headers)
        soup = BeautifulSoup(result.text, "html.parser")

        jobs = []
        for card in soup.select(".job__title"):
            title_tag = card.select_one(".job__title b")
            link_tag = card.select_one(".job__title a")
            url_suffix = link_tag['href'] if link_tag else ""

            job_url = "https://relocate.me" + url_suffix
            job_result = requests.get(job_url, headers=headers)
            soup = BeautifulSoup(job_result.text, "html.parser")
            description_block = soup.select_one(".job-info__description")  # may vary

            jobs.append({
                "title": title_tag.text.strip() if title_tag else "N/A",
                "link": job_url,
                "description": description_block.get_text(separator="\n").strip() if description_block else "No job description found."
            })
        return jobs

    except Exception as e:
        return {}


def extract_text_from_pdf(pdf_file):
    doc = fitz.open(stream=pdf_file.read(), filetype="pdf")
    text = ""
    for page in doc:
        text += page.get_text()
    return text
