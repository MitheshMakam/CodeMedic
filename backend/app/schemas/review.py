from enum import Enum
from pydantic import BaseModel, Field, field_validator

class RepositoryRequest(BaseModel):
    repository_url: str = Field(min_length=3, max_length=500, description="Public GitHub repository URL")

    @field_validator("repository_url")
    @classmethod
    def normalize_url(cls, value: str) -> str:
        value = value.strip()
        if value.startswith("github.com/"):
            value = f"https://{value}"
        return value.rstrip("/")

class ExplainRequest(RepositoryRequest):
    path: str = Field(min_length=1, max_length=500)
    symbol: str | None = Field(default=None, max_length=200)

class CommitRequest(BaseModel):
    diff: str = Field(min_length=1, max_length=50_000)

class FindingSeverity(str, Enum):
    critical = "critical"
    high = "high"
    medium = "medium"
    low = "low"
    info = "info"

class Finding(BaseModel):
    title: str
    severity: FindingSeverity = FindingSeverity.info
    path: str | None = None
    line: int | None = None
    description: str
    recommendation: str

class RepositorySnapshot(BaseModel):
    name: str
    url: str
    default_branch: str = "main"
    file_count: int
    languages: list[str] = []
    files: list[str] = []
    tree: dict[str, list[str]] = {}

class ReviewResponse(BaseModel):
    title: str
    overview: str
    markdown: str
    findings: list[Finding] = []
    snapshot: RepositorySnapshot | None = None
    ai_enriched: bool = False

class ProgressEvent(BaseModel):
    step: str
    status: str
    message: str
    data: ReviewResponse | None = None
