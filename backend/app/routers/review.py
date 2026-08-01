import json
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
from app.schemas.review import CommitRequest, ExplainRequest, RepositoryRequest, ReviewResponse
from app.services.openai_service import OpenAIReviewService
from app.services.orchestrator import ReviewOrchestrator
from app.services.repository import RepositoryService
from app.services.scanner import scan

router = APIRouter(tags=["reviews"])

def context(request: RepositoryRequest):
    return RepositoryService().snapshot(request.repository_url)

def make_handler(kind: str, security_only: bool = False):
    def handler(request: RepositoryRequest) -> ReviewResponse:
        snapshot, source = context(request)
        return OpenAIReviewService().review(kind, snapshot, source, scan(source, security_only=security_only))
    return handler

router.post("/analyze", response_model=ReviewResponse)(make_handler("analysis"))
router.post("/summary", response_model=ReviewResponse)(make_handler("repository summary"))
router.post("/bugs", response_model=ReviewResponse)(make_handler("bug detection"))
router.post("/security", response_model=ReviewResponse)(make_handler("security review", True))
router.post("/tests", response_model=ReviewResponse)(make_handler("unit test plan"))
router.post("/readme", response_model=ReviewResponse)(make_handler("README generator"))
@router.post("/improve", response_model=None)
def improve(request: RepositoryRequest):
    def events():
        yield 'data: {"step":"analyze","status":"running","message":"Connecting to GitHub and fetching repository files"}\n\n'
        try:
            snapshot, source = context(request)
            for event in ReviewOrchestrator().run(snapshot, source):
                yield f"data: {event.model_dump_json()}\n\n"
        except Exception as exc:
            yield f"data: {json.dumps({'step': 'analyze', 'status': 'error', 'message': str(getattr(exc, 'detail', 'Repository review failed.'))})}\n\n"
    return StreamingResponse(events(), media_type="text/event-stream", headers={"Cache-Control":"no-cache", "X-Accel-Buffering":"no"})

@router.post("/explain", response_model=ReviewResponse)
def explain(request: ExplainRequest) -> ReviewResponse:
    snapshot, source = context(request)
    if request.path not in source:
        from fastapi import HTTPException
        raise HTTPException(404, "The requested text file was not found or is too large to inspect.")
    focused = {request.path: source[request.path]}
    kind = f"explanation for {request.symbol or request.path}"
    return OpenAIReviewService().review(kind, snapshot, focused, [])

@router.post("/commit", response_model=ReviewResponse)
def commit(request: CommitRequest) -> ReviewResponse:
    from app.schemas.review import RepositorySnapshot
    snapshot = RepositorySnapshot(name="Uncommitted changes", url="https://github.com", file_count=0)
    return OpenAIReviewService().review("conventional commit message", snapshot, {"diff.patch": request.diff}, [])
