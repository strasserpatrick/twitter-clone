from fastapi import FastAPI

from owntwitter.api.endpoints import router
from owntwitter.models.settings import Settings

settings = Settings()
app = FastAPI()
app.include_router(router)

if __name__ == "__main__":

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=settings.uvicorn_port)
