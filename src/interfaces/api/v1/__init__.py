from fastapi import APIRouter
from ....modules.fighter.routes import router as fighter_router


router=APIRouter(prefix="/v1")
router.include_router(fighter_router,prefix="/fighters")
