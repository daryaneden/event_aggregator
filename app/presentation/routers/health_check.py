from fastapi import APIRouter

router = APIRouter(prefix='/api', tags=["health_check"])

@router.get("/health", status_code=200)
async def health_check():
    return {"status": "ok"}