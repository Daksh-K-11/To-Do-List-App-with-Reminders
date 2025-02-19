from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db

from ..schema import auth_schema

router = APIRouter(prefix="/login", tags=["Authentication"])

@router.post('/login', response_model=auth_schema.Token, status_code=status.HTTP_200_OK)
def login(user: auth_schema.Login, db: Session = Depends(get_db)):
    return