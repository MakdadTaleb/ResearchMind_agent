from http.client import HTTPException
from fastapi import APIRouter, Request, Depends
from api.auth import get_current_user
from fastapi.responses import StreamingResponse
from api.schemas.research import ResearchRequest, ResearchResponse
from api.services import research as research_service
from api.limiter import limiter
from repositories.reports_repository import get_user_reports, get_report_by_id



router = APIRouter(prefix="/research", tags=["research"])


@router.post("", response_model=ResearchResponse)
@limiter.limit("5/minute")
async def run_research(request: Request, body: ResearchRequest, user=Depends(get_current_user)):
    return await research_service.run_research(body.topic, user.id)


@router.post("/stream")
@limiter.limit("5/minute")
async def run_research_stream(request: Request, body: ResearchRequest, user=Depends(get_current_user)):
    generator = await research_service.run_research_stream(body.topic, user.id)
    return StreamingResponse(
        generator,
        media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"}
    )


@router.get("/reports")
async def list_reports(user=Depends(get_current_user)):
    return await get_user_reports(user.id)


@router.get("/reports/{report_id}")
async def get_report(report_id: str, user=Depends(get_current_user)):
    report = await get_report_by_id(report_id, user.id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found.")
    return report