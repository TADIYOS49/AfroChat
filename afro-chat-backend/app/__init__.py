from fastapi import FastAPI, Request
from config import Config, initial_config
from app.routers import api_v1_router
from app.utils.logger import fast_api_logger, sqlalchemy_logger


async def logger_middleware(request: Request, call_next):
    request.state.logger = fast_api_logger
    response = await call_next(request)
    return response


async def shutdown_event():
    fast_api_logger.info("Shutting down...")


async def startup_event():
    fast_api_logger.info("Starting up...")


def create_app(config: Config) -> FastAPI:
    print(config.CONFIG_TYPE)
    app = FastAPI()
    app.include_router(api_v1_router)
    app.middleware('http')(logger_middleware)
    app.on_event('shutdown')(shutdown_event)
    app.on_event('startup')(startup_event)

    return app
