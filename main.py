import uvicorn
from fastapi import FastAPI

import router
from app.config.migrate import migrate
from app.config.seed import seed


def create_app() -> FastAPI:
    app = FastAPI()
    app.include_router(router.router)
    return app


app = create_app()
migrate()
seed()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
