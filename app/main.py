from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes import auth, users
from app.core.config import settings
from app.db.init_db import init_db
from app.api.routes import auth, case_images, cases, users

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(title=settings.PROJECT_NAME, version="0.1.0", lifespan=lifespan)

app.include_router(auth.router, prefix="/api/v1/auth", tags=["Auth"])
app.include_router(users.router, prefix="/api/v1/users", tags=["Users (admin)"])

app.include_router(cases.router, prefix="/api/v1/cases", tags=["Cases"])
app.include_router(case_images.router, prefix="/api/v1/cases", tags=["Case images"])

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok"}