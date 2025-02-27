from fastapi import HTTPException, APIRouter, Depends, status
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from .. import utils, oauth2
from ..schemas import auth_schema
from ..dependency import get_current_user

router = APIRouter(tags=["Authentication"], prefix='/login')

@router.post('/', response_model=auth_schema.Token, status_code=status.HTTP_200_OK)
def login(user_credential: auth_schema.Login, db: Session = Depends(get_db)):

    
    user = db.query(User).filter(User.email == user_credential.email).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No such email id")
    
    if not utils.verify(user_credential.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect password")
    
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.patch('/', status_code=status.HTTP_202_ACCEPTED)
def change_password(pwd_change: auth_schema.ChangePassword, db: Session=Depends(get_db), current_user=Depends(get_current_user)):
    if not utils.verify(pwd_change.current_password, current_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect old password")
    
    current_user.password = utils.get_password_hash(pwd_change.new_password)
    db.commit()
    db.refresh(current_user)
    
    return {"message": "Password updated successfully"}