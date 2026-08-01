import re
from fastapi import HTTPException

GITHUB_URL = re.compile(r"^https?://github\.com/([^/]+)/([^/#?]+?)(?:\.git)?/?$")

def parse_github_url(url: str) -> tuple[str, str]:
    match = GITHUB_URL.match(url)
    if not match:
        raise HTTPException(422, "Provide a public GitHub repository URL such as https://github.com/owner/repository")
    return match.group(1), match.group(2)
