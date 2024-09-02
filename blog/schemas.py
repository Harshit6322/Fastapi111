from pydantic import BaseModel

class Blog(BaseModel):
    title : str
    body :str

class User(BaseModel):
    name : str
    email :str
    password : str

class showblog(BaseModel):
    title : str
    body :str

    class Config:
        orm_mode =True

class showUser(BaseModel):
    name : str
    email :str

    class Config:
        orm_mode =True


