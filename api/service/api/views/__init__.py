from fastapi import FastAPI, APIRouter

from . import root
from ..models import View


def add_view(
    app: FastAPI,
    view: View
) -> None:
    if view.prefix is None:
        app.include_router(view.router, dependencies=view.PROTECTED)
        app.include_router(view.not_protect_router)
        return

    app.include_router(view.router,
                       prefix=view.prefix,
                       dependencies=view.PROTECTED)
    app.include_router(view.not_protect_router, prefix=view.prefix)


def add_views(app: FastAPI) -> None:
    add_view(app, root.view)

