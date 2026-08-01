import logging
from collections import defaultdict
from github import Github, Auth
from fastapi import HTTPException
from app.core.config import get_settings
from app.schemas.review import RepositorySnapshot
from app.utils.github import parse_github_url

logger = logging.getLogger(__name__)
SKIPPED = {"node_modules", ".git", "dist", "build", ".next", "vendor", "coverage"}
TEXT_EXTENSIONS = {".py", ".js", ".jsx", ".ts", ".tsx", ".go", ".java", ".rb", ".php", ".cs", ".rs", ".vue", ".html", ".css", ".sql", ".yml", ".yaml", ".json", ".md"}

class RepositoryService:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = Github(auth=Auth.Token(settings.github_token)) if settings.github_token else Github()
        self.settings = settings

    def snapshot(self, url: str) -> tuple[RepositorySnapshot, dict[str, str]]:
        owner, repo_name = parse_github_url(url)
        try:
            repo = self.client.get_repo(f"{owner}/{repo_name}")
            contents = repo.get_contents("")
        except Exception as exc:
            logger.warning("Unable to read repository %s: %s", url, exc)
            raise HTTPException(404, "Repository could not be read. Confirm it is public and the URL is correct.") from exc
        paths, source, tree = [], {}, defaultdict(list)
        queue = list(contents)
        while queue and len(paths) < self.settings.max_repository_files:
            item = queue.pop(0)
            if any(part in SKIPPED for part in item.path.split("/")):
                continue
            if item.type == "dir":
                try: queue.extend(repo.get_contents(item.path))
                except Exception: continue
                continue
            paths.append(item.path)
            parent = item.path.split("/")[0] if "/" in item.path else "root"
            tree[parent].append(item.path)
            ext = "." + item.path.rsplit(".", 1)[-1].lower() if "." in item.path else ""
            if ext in TEXT_EXTENSIONS and item.size <= self.settings.max_file_bytes:
                try: source[item.path] = item.decoded_content.decode("utf-8", errors="replace")
                except Exception: pass
        languages = list((repo.get_languages() or {}).keys())
        return RepositorySnapshot(name=repo.full_name, url=url, default_branch=repo.default_branch, file_count=len(paths), languages=languages, files=paths, tree=dict(tree)), source
