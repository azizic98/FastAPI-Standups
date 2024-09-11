import logging
from typing import AsyncGenerator, Dict

import models
from config import settings
from database import SessionLocal, engine
from fastapi import Depends, FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from models import User, UserRole
from routers import auth, sql_injection_demo, standups, users
from sqlalchemy.orm import Session
from utils import hash_password

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_tables():
    try:
        logger.info("Creating tables...")
        models.Base.metadata.create_all(bind=engine)
        logger.info("Tables created.")
    except Exception as e:
        logger.error(f"Error creating tables: {e}")


def create_admin_user(db: Session):
    admin_exists = db.query(User).filter(User.role == UserRole.Admin.value).first()
    if not admin_exists:
        hashed_password = hash_password(settings.ADMIN_PASSWORD)
        admin = User(
            email=settings.ADMIN_USER,
            password=hashed_password,
            role=UserRole.Admin.value,
        )
        db.add(admin)
        db.commit()
        logger.info("Admin user created.")
    else:
        logger.info("Admin user already exists.")


async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Log Start-Up
    logger.info("Application is starting up...")

    # Create database tables
    create_tables()

    # Create admin user
    db = SessionLocal()
    try:
        create_admin_user(db)
    finally:
        db.close()

    yield

    # Log Shut-Down
    logger.info("Application is shutting down...")


app = FastAPI(lifespan=lifespan)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(auth.router)
app.include_router(standups.router)
app.include_router(sql_injection_demo.router)


@app.get("/", status_code=status.HTTP_200_OK)
def get_check() -> Dict:
    return dict(status="OK!!")
