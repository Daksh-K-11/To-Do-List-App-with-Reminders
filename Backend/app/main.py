from fastapi import FastAPI
from  . import models
from .database import engine
from .routers import auth, user

models.Base.metadata.create_all(bind=engine)
app = FastAPI()

app.include_router(auth.router)
app.include_router(user.router)

@app.get('/')
def root():
    return {"message" : "Hey there it's me"}