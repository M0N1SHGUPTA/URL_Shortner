from fastapi import APIRouter, Depends
from schemas import create_user, login_user
from services import auth as auth_service
from database import get_db
from sqlalchemy.orm import Session

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/create_user")
def createUser(data: create_user,db: Session = Depends(get_db)):
    return auth_service.create_user(data, db)

@router.post("/login")
def login(data: login_user, db: Session = Depends(get_db)):
    return auth_service.login_user(data, db)
