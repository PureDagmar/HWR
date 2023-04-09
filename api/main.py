import logging

import uvicorn

from service.api.app import create_app
from service.settings import get_config

config = get_config()
app = create_app(config)


if __name__ == "__main__":
    host = "0.0.0.0"
    port = config.PORT
    workers = config.WORKERS
    reload = config.RELOAD
    if reload:
        logging.info(f"RUN AS UVICORN INSTANCE. RELOAD")
        uvicorn.run("main:app", host=host, port=port, reload=reload)
    else:
        logging.info(f"RUN AS UVICORN INSTANCE. WORKERS: {workers}")
        uvicorn.run("main:app", host=host, port=port, workers=workers)
