from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas import auth_schema, user_schema
from ..utils import hash
from .auth import login

router = APIRouter(prefix="/user", tags=["User"])

@router.post("/", response_model=auth_schema.Token, status_code=status.HTTP_201_CREATED)
def create_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    
    if db.query(User).filter(User.email == user.email).first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    pwd = user.password                   # stored so that the entered pwd can be sent in login
    user.password = hash(user.password)
    
    new_user = User(**user.model_dump())
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    login_user = auth_schema.Login(email=new_user.email, password=pwd)
    
    login(login_user, db)