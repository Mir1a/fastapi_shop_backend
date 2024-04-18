from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

from src.product.routers import router as product_router

app = FastAPI(
    title="Shop-backend"
)

app.include_router(product_router)