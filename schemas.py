from pydantic import BaseModel, EmailStr

class url(BaseModel):
    og_url: str 


class create_user(BaseModel):
    name: str
    email: EmailStr
    password: str


class login_user(BaseModel):
    email: EmailStr
    password: str