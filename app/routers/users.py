from .. import models, schemas
from fastapi import status, HTTPException, Depends, APIRouter
from ..database import Base, engine, get_db
from starlette.status import HTTP_404_NOT_FOUND
from ..schemas import UserCreate
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(
    prefix = '/users',
    tags = ['users']
)

@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: UserCreate, db: Session = Depends(get_db)):

    user.password = utils.hash(user.password)
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model=schemas.User)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail=f'User with {id} not found')
    return user