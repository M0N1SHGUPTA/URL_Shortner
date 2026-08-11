from fastapi import Depends
from sqlalchemy.orm import Session
from database import get_db
from schemas import create_user, login_user
from models import Users
import hashlib
import jwt


#Login User
def login_user(data: login_user, db: Session):
    user = db.query(Users).filter(Users.email == data.email).first()

    if user is None:
        return {
            "message": "User Does Not Exist In SYSTEM"
        }

    user_password = hashlib.sha256(data.password.encode()).hexdigest()

    if user.password == user_password:
        return {
            "message": "login Sucessfull"
        }
    else:
        return{
            "message": "Incorrect Password"
        }


#Create User
def create_user(data: create_user, db: Session):

    user = db.query(Users).filter(Users.email == data.email).first()

    if user:
        return {
            "error" :"User already exists"
        }

    hashed_password = hashlib.sha256(data.password.encode()).hexdigest()

    new_user = Users(
        name = data.name,
        email = data.email,
        password = hashed_password
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Account Creation Successfull",
        "new_user": new_user
    }
