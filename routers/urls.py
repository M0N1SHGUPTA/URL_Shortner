from fastapi import APIRouter, Depends
from schemas import url
from services import urls as url_services
from sqlalchemy.orm import Session
from database import get_db

router = APIRouter(prefix="/urls", tags=["urls"])


@router.post('/v1/url/')
def shorten_url(data: url, db: Session = Depends(get_db)):
    return url_services.shorten(data, db)

@router.get("/{short_code}")
def get_url(short_code: str, db: Session = Depends(get_db)):
    return url_services.get_short_url(short_code, db)

