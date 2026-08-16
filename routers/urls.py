from fastapi import APIRouter, Depends
from schemas import url
from services import urls as url_services
from sqlalchemy.orm import Session
from database import get_db
from services.auth import getCurretUser

router = APIRouter(prefix="", tags=["urls"])


@router.post('/short')
def shorten_url(
    data: url, 
    db: Session = Depends(get_db),
    current_user: dict = Depends(getCurretUser)
):
    print(f"SHortening URL for {current_user['email']}")
    return url_services.shorten(data, db, current_user['user_id'])



@router.get("/urls")
def get_all_urls(db: Session = Depends(get_db), current_user: dict = Depends(getCurretUser)):
    print(f"printing all URLs for the user: {current_user['email']}")

    return url_services.get_all_urls(db, current_user['user_id'])

@router.get("/{short_code}")
def get_url(short_code: str, db: Session = Depends(get_db)):
    return url_services.get_short_url(short_code, db)
