from fastapi import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas import url
from models import urls

import hashlib

def shorten(data: url, db:Session, user_id: int):

    check_url = db.query(urls).filter(
        urls.long_url == data.og_url,
        urls.user_id == user_id
        ).first()

    if check_url:
        return check_url.short_url

    #Creating Short URL
    short_url = hashlib.sha256(data.og_url.encode()).hexdigest()
    result_url = short_url[:7]

    new_url = urls(
        long_url = data.og_url,
        short_url = result_url,
        user_id = user_id
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)


    return new_url


def get_short_url(short_code:str, db:Session):

    db_url = db.query(urls).filter(urls.short_url == short_code).first()

    if not db_url:
        return {
            "error": "URL not Found"
        }

    return RedirectResponse(
        url=db_url.long_url,
        status_code=307
    )

def get_all_urls(db: Session, user_id: int):

    url_data = db.query(urls).filter(urls.user_id == user_id).all()

    if not url_data:
        return {
            'message' :"You havnt played enough"
        }
    
    return url_data