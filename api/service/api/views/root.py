import typing as tp

from fastapi import APIRouter, Depends, UploadFile

from ..models import View
from ..token import has_access
from ...settings import get_config

view_prefix = ''

router = APIRouter()
not_protect_router = APIRouter()

sc = get_config()
PROTECTED = [Depends(has_access)]


@not_protect_router.get(path="/health", tags=["Health"])
async def health() -> str:
    return "I am alive"


@router.post(path="/inference", tags=["Inference"])
async def inference(blank: UploadFile) -> tp.Dict:
    pass


view = View(
    router=router,
    not_protect_router=not_protect_router,
    prefix=view_prefix,
    PROTECTED=PROTECTED
)
