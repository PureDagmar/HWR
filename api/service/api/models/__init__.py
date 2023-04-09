import typing as tp

from fastapi import APIRouter
from pydantic import BaseModel


class Error(BaseModel):
    error_key: str
    error_message: str
    error_loc: tp.Optional[tp.Any] = None


class View:
    def __init__(
        self,
        router: APIRouter,
        not_protect_router: APIRouter,
        prefix: str,
        PROTECTED: callable
    ):
        self.PROTECTED = PROTECTED
        self.prefix = prefix
        self.not_protect_router = not_protect_router
        self.router = router
