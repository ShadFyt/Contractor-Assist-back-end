from fastapi import APIRouter, status, Depends, HTTPException
from sqlmodel import Session, SQLModel, Field, select
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from jose import JWTError, jwt
from typing import List, Optional
from config import settings
from datetime import datetime, timedelta

from models.db import get_session

from pydantic import BaseModel


fake_users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "johndoe@example.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class BaseUser(SQLModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(BaseUser, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str

    def verify_password(self, plain_password: str):
        return pwd_context.verify(plain_password, self.hashed_password)


class UserRead(BaseUser):
    id: int


class UserCreate(BaseUser):
    password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin")

router = APIRouter(prefix="/admin", tags=["admin"])


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(user, password: str):
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode["exp"] = expire
    return jwt.encode(to_encode, settings.SECRET_KEY, settings.ALGORITHM)


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        raise credentials_exception from e
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: UserRead = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


def create_owner(owner: UserRead, session: Session):
    owner_obj = UserInDB(
        username=owner.username, hashed_password=pwd_context.hash(owner.hashed_password)
    )
    session.add(owner_obj)
    session.commit()
    session.refresh(owner_obj)
    return owner_obj


@router.post("/")
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    new_user = UserInDB(hashed_password=user.password, username=user.username)
    new_user.hashed_password = get_password_hash(user.password)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)
    return new_user


@router.post("/token", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    print("data is ", form_data)
    db_user = select(UserInDB).where(UserInDB.username == form_data.username)
    user = session.exec(db_user).one_or_none()

    if not user.verify_password(form_data.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=30)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    print("LOGGIN :", access_token)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me")
async def read_users_me(current_user: UserRead = Depends(get_current_active_user)):
    return current_user
