import json
import logging
from openai import OpenAI
from app.core.config import get_settings
from app.schemas.review import Finding, FindingSeverity, RepositorySnapshot, ReviewResponse

logger = logging.getLogger(__name__)

class OpenAIReviewService:
    def __init__(self) -> None:
        settings = get_settings()
        self.client = OpenAI(api_key=settings.openai_api_key) if settings.openai_api_key else None
        self.model = settings.openai_model

    def review(self, kind: str, snapshot: RepositorySnapshot, source: dict[str, str], preflight: list[Finding]) -> ReviewResponse:
        overview = f"{snapshot.name} contains {snapshot.file_count} inspected files and uses {', '.join(snapshot.languages) or 'an undetected stack'}."
        if not self.client:
            return ReviewResponse(title=kind.title(), overview=overview, markdown=self._fallback(kind, snapshot, preflight), findings=preflight, snapshot=snapshot)
        excerpts = "\n\n".join(f"### {path}\n{body[:5000]}" for path, body in list(source.items())[:25])
        prompt = f"""You are CodeMedic, a precise senior repository reviewer. Produce a {kind} review.
Repository: {snapshot.model_dump_json()}
Preflight findings: {[item.model_dump() for item in preflight]}
Source excerpts:\n{excerpts}
Return JSON only with overview, markdown, findings. Findings must have title, severity (critical/high/medium/low/info), path, line, description, recommendation. Markdown must be useful, concise, and specific."""
        try:
            completion = self.client.chat.completions.create(model=self.model, messages=[{"role":"system","content":"Return valid JSON only."}, {"role":"user","content":prompt}], response_format={"type":"json_object"}, temperature=0.2)
            payload = json.loads(completion.choices[0].message.content or "{}")
            findings = [Finding(**item) for item in payload.get("findings", [])]
            return ReviewResponse(title=kind.title(), overview=payload.get("overview", overview), markdown=payload.get("markdown", self._fallback(kind, snapshot, preflight)), findings=findings or preflight, snapshot=snapshot, ai_enriched=True)
        except Exception as exc:
            logger.exception("AI review failed: %s", exc)
            return ReviewResponse(title=kind.title(), overview=overview, markdown=self._fallback(kind, snapshot, preflight) + "\n\n> AI enrichment was unavailable; this is the deterministic preflight report.", findings=preflight, snapshot=snapshot)

    @staticmethod
    def _fallback(kind: str, snapshot: RepositorySnapshot, findings: list[Finding]) -> str:
        issue_lines = "\n".join(f"- **{item.severity.value.upper()}** `{item.path or 'repository'}`: {item.title} — {item.recommendation}" for item in findings) or "- No rule-based issues were detected in the inspected text files."
        return f"## {kind.title()} report\n\n**Repository:** [{snapshot.name}]({snapshot.url})  \n**Stack:** {', '.join(snapshot.languages) or 'Not detected'}  \n**Files inspected:** {snapshot.file_count}\n\n### Findings\n{issue_lines}\n\n### Recommended next steps\n1. Validate findings against runtime context.\n2. Add focused tests around changed behavior.\n3. Re-run this review after remediation."
