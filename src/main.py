import os

from fastapi import Depends, FastAPI, HTTPException, UploadFile, File
from sqlalchemy.orm import Session


from s3 import upload_file, download_file
from src.transaction.routers import router as transactions_router
from src.product.routers import router as product_router
from src.product import models, schemas
from .database import async_sessionmaker
from src.user.routers import router as user_router
from .user.base_config import fastapi_users, auth_backend, current_user
from .user.schemas import UserRead, UserCreate
from .user import models
import logging
from fastapi import FastAPI

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Shop-backend"
)


@app.post("/upload/")
async def upload_to_s3(file: UploadFile = File(...)):
    file_location = f"/tmp/{file.filename}"
    with open(file_location, "wb") as f:
        f.write(await file.read())

    upload_response = upload_file(file_location, BUCKET_NAME, file.filename)
    if upload_response is None:
        raise HTTPException(status_code=500, detail="Upload failed")
    return {"filename": file.filename}


@app.get("/download/")
async def download_from_s3(filename: str):
    file_content = download_file(f"/tmp/{filename}", BUCKET_NAME, filename)
    if file_content is None:
        raise HTTPException(status_code=404, detail="File not found")
    return {"filename": filename, "content": file_content.decode('utf-8')}


BUCKET_NAME = os.getenv('S3_BUCKET_NAME')


@app.get("/")
def read_root():
    return {"message": "Hello, World!"}


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
    # redis = aioredis.from_url("redis://localhost")
    # FastAPICache.init(RedisBackend(redis), prefix="fastapi-cache")
    pass


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)