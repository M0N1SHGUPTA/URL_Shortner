from fastapi import Depends
from fastapi import HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from database import get_db
from schemas import create_user, login_user
from models import Users
import hashlib
import jwt
import os
from dotenv import load_dotenv
import datetime

load_dotenv()
SECRET_KEY = os.getenv("Secret_Key", "KingMonish")

#it gets the token from the request header's authoorization 
security = HTTPBearer()

#Login User
def login_user(data: login_user, db: Session):

    # Verify Password
    user = db.query(Users).filter(Users.email == data.email).first()

    if user is None:
        return {
            "message": "User Does Not Exist In SYSTEM"
        }

    user_password = hashlib.sha256(data.password.encode()).hexdigest()

    payload = {}

    if user.password == user_password:
        payload["user_id"] = user.id
        payload["email"] = user.email
        payload["exp"] = datetime.datetime.utcnow() + datetime.timedelta(minutes = 50000)
    else:
        return{
            "message": "Incorrect Password"
        }

    # Create Payload

    token = jwt.encode(
        payload,
        SECRET_KEY,
        algorithm="HS256"
    )

    return {
        "access": token,
        "token_type": "bearer"
    }



def verifyToken(token : str):

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

        return payload
    
    except jwt.ExpiredSignatureError:
        return {
            "error": "Token has expired."
        }
    except jwt.InvalidTokenError:
        return {
            "error": "Invalid Token Error."
        }

#Create User
def create_user(data: create_user, db: Session):
    
    user = db.query(Users).filter(Users.email == data.email).first()

    if user:
        raise HTTPException(
            status_code = status.HTTP_409_CONFLICT,
            detail = "User Already Exists."
        )

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


def getCurretUser(credentials: HTTPAuthorizationCredentials = Depends(security)):
    #1.extract the raw token string
    token = credentials.credentials

    #2.verify the token using 
    payload = verifyToken(token)


    #3.if there is an error in verification, raise an HTTP 401 unauthorized exception
    if "error" in payload:
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = payload["error"],
            headers = {"WWW-Authenticate": "Bearer"}
        )

    #4. return the payload which contains userid, email
    return payload