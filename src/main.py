from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from src.product.routers import router as product_router
from src.product import models, schemas
from . import crud
from .database import async_sessionmaker

app = FastAPI(
    title="Shop-backend"
)

def get_db():
    db = async_sessionmaker()
    try:
        yield db
    finally:
        db.close()


app.include_router(product_router)