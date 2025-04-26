from datetime import datetime, timedelta, timezone
from typing import Annotated

from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, ValidationError
from app.config import settings

from app.database.models.user import User
from app.database.models.account import Account
from fastapi import Request, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from app.utility import _encode_jwt, _decode_jwt, JWTBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)



def create_access_token(user: User, accounts: list[Account]):
    # Create payload
    accounts_payload = []
    for account in accounts:
        accounts_payload.append(
            {
                "id": str(account.id),
                "full_name": account.full_name,
                "email": account.email,
                "email_verified": account.email_verified,
                "phone_number": account.phone_number,
                "phone_number_verified": account.phone_number_verified,
                "status": account.status,
                "is_primary": account.is_primary,
                "created_at": account.created_at,
                "updated_at": account.updated_at,
            }
        )
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
        "accounts": accounts_payload,
    }
    # Create access token
    access_token_expires = timedelta(
        minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = _encode_jwt(
        data=payload, expires_delta=access_token_expires
    )
    return access_token


def create_refresh_token(user: User):
    # Create payload
    payload = {
        "sub": str(user.id),
        "username": user.username,
        "created_at": user.created_at,
        "updated_at": user.updated_at,
    }
    # Create refresh token
    refresh_token_expires = timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    refresh_token = _encode_jwt(
        data=payload, expires_delta=refresh_token_expires
    )
    return refresh_token
