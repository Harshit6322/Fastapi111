from fastapi import FastAPI,Depends,status
from fastapi.exceptions import HTTPException
from .database import engine,SessionLocal
from .import models,schemas
from sqlalchemy.orm import Session
from typing import List
from .hashing import hash
app = FastAPI()

models.Base.metadata.create_all(bind=engine)


def get_db():

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "chacha"}

@app.post("/blog/",status_code=status.HTTP_201_CREATED)
def create_item(request: schemas.Blog,db:Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title,body=request.body,owner_id=6322)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/blog',response_model=List[schemas.showblog],tags=['Blogs'])
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs 

@app.get('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.showblog,tags=['Blogs'])
def all(id,db:Session = Depends(get_db),status_code=status.HTTP_200_OK):
    blogs = db.query(models.Blog).filter(models.Blog.id ==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog {id} not found")
    return blogs 

@app.delete('/blog/{id}',status_code=status.HTTP_204_NO_CONTENT,tags=['Blogs'])
def distroy(id,db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id ==id)

    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog {id} not found")
    blogs.delete(synchronize_session=False)
    db.commit()

    return 'done'

@app.put('/blog/{id}',status_code=status.HTTP_202_ACCEPTED,tags=['Blogs'])
def update(id,request:schemas.Blog,db:Session = Depends(get_db)):
    blogs = db.query(models.Blog).filter(models.Blog.id ==id)

    if not blogs.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog {id} not found")
    blogs.update(dict(request))
    db.commit()

    return 'ok'



@app.get('/User',response_model=List[schemas.showUser],tags=['Users'])
def all(db:Session = Depends(get_db)):
    blogs = db.query(models.User).all()
    return blogs 

@app.post("/User/",status_code=status.HTTP_201_CREATED,response_model=schemas.showUser,tags=['Users'])
def create_item(request: schemas.User,db:Session = Depends(get_db)):
    
    new_blog = models.User(name=request.name,email=request.email,password=hash.bcrypt(request.password))
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog

@app.get('/User/{id}',status_code=status.HTTP_202_ACCEPTED,response_model=schemas.showUser,tags=['Users'])
def all(id,db:Session = Depends(get_db),status_code=status.HTTP_200_OK):
    blogs = db.query(models.User).filter(models.User.id ==id).first()
    if not blogs:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"blog {id} not found")
    return blogs 