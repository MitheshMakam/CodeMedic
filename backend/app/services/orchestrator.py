from collections.abc import Iterator
from app.schemas.review import ProgressEvent, RepositorySnapshot, ReviewResponse
from app.services.openai_service import OpenAIReviewService
from app.services.scanner import scan

class ReviewOrchestrator:
    stages = [("analyze", "Analyzing repository structure"), ("summary", "Creating architecture summary"), ("bugs", "Detecting bugs and code smells"), ("security", "Reviewing security posture"), ("readme", "Generating documentation"), ("tests", "Generating test strategy"), ("improve", "Prioritizing improvements")]
    def __init__(self) -> None: self.ai = OpenAIReviewService()

    def run(self, snapshot: RepositorySnapshot, source: dict[str, str]) -> Iterator[ProgressEvent]:
        for stage, message in self.stages:
            yield ProgressEvent(step=stage, status="running", message=message)
            findings = scan(source, security_only=stage == "security") if stage in {"bugs", "security", "analyze"} else []
            report = self.ai.review(stage, snapshot, source, findings)
            yield ProgressEvent(step=stage, status="completed", message=f"{stage.title()} complete", data=report)
