from fastapi import Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from database import get_db
from schemas import url
from models import urls

import hashlib

def shorten(data: url, db:Session):

    check_url = db.query(urls).filter(urls.long_url == data.og_url).first()

    if check_url:
        return check_url.short_url

    #Creating Short URL
    short_url = hashlib.sha256(data.og_url.encode()).hexdigest()
    result_url = short_url[:7]

    new_url = urls(
        long_url = data.og_url,
        short_url = result_url
    )

    db.add(new_url)
    db.commit()
    db.refresh(new_url)


    return new_url


def get_short_url(short_code:str, db:Session):

    db_url = db.query(urls).filter(urls.short_url == short_code).first()

    long_url = db_url.long_url

    if not long_url:
        return {
            "error": "URL not Found"
        }

    return RedirectResponse(
        url=long_url,
        status_code=307
    )
