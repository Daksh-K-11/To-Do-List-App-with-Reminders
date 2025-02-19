from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from .. import utils, oauth2
from ..schemas import auth_schema

router = APIRouter(tags=["Authentication"])

@router.post('/login', response_model=auth_schema.Token, status_code=status.HTTP_200_OK)
def login(user_credential: auth_schema.Login, db: Session = Depends(get_db)):

    
    user = db.query(User).filter(User.email == user_credential.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such email id")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    
    access_token = oauth2.create_access_token(data={"id": user.id, "email": user.email[:5]})
    
    return {"access_token": access_token, "token_type": "bearer"}