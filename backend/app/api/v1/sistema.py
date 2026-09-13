from fastapi import APIRouter

router = APIRouter(tags=["sistema"])


@router.get("/health", summary="Estado del servicio")
def health() -> dict[str, str]:
    return {"estado": "ok"}
