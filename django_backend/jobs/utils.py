import requests


def search_jobs_from_remoteok(title, skills):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/112.0.0.0 Safari/537.36"
    }
    # search_keywords = [title] + skills[:3]  # Limit to first 3 skills
    search_keywords = skills[:1]
    # lowercase_list = [item.lower() for item in search_keywords]
    query = "+".join(search_keywords)
    url = f"https://remoteok.com/api?tags={query}"
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()[1:]  # First item is metadata
    return []
