from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis

from src.transaction.routers import router as transactions_router
from src.product.routers import router as product_router
from src.product import models, schemas
from .database import async_sessionmaker
from src.user.routers import router as user_router
from .user.base_config import fastapi_users, auth_backend, current_user
from .user.schemas import UserRead, UserCreate
from .user import models

app = FastAPI(
    title="Shop-backend"
)


def get_db():
    db = async_sessionmaker()
    try:
        yield db
    finally:
        db.close()


app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
app.include_router(product_router)
app.include_router(transactions_router)
app.include_router(user_router)


@app.on_event("startup")
async def startup():
    redis = aioredis.from_url("redis://localhost")
    FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")