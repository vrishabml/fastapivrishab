from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer, oauth2
from sqlalchemy.orm.session import Session
from . import config
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

from app import models, schemas, database

#SECRET_KEY
#Algorithm
#Expiration time


SECRET_KEY = config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = config.settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try: 
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: str = payload.get("user_id")
        if not id:
            raise credentials_exception
        token_data = schemas.TokenData(id= id)
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str =  Depends(oauth2_scheme),db: Session =  Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == token.id).first()

    return user
