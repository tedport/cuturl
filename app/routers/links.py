from fastapi import APIRouter

router = APIRouter(prefix="links", tags="links")

@router.post("/create")
def create_shortcut():
    return {}