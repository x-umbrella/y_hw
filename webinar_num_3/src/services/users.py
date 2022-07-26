from functools import lru_cache
from fastapi import Depends
from sqlmodel import Session
from werkzeug.security import generate_password_hash, check_password_hash
from src.api.v1.schemas import UserCreate, UserLogin, UserMe, UserEmail
from src.db import AbstractCache, get_cache, get_session
from src.models import User
from src.core import config_auth
from src.services import ServiceMixin


__all__ = ("UserService", "get_user_service")


class UserService(ServiceMixin):

    def get_user(self, username: str) -> User:
        return (
            self.session.query(User).filter(User.username == username).first()
        )

    def create_user(self, user_data: UserCreate) -> dict:
        user = User(
            email=user_data.email,
            username=user_data.username,
            password=generate_password_hash(user_data.password),
        )
        if self.get_user(user.username):
            return {"error": f"User {user.username} already registered"}
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)

        if self.get_user(user.username):
            return {"msg": "User Created.", "user": user}    
        
    def login(self, _jwt, user: UserLogin) -> dict:
        _user = self.get_user(user.username)
        if not _user:
            return {'error': 'User does not exist'}
        if not check_password_hash(_user.password, user.password):
            return {'error': 'Wrong password'}

        tokens = {'access_token': _jwt.create_access_token(subject=user.username,
                expires_time=config_auth.JWT_A_EX_S),
                'refresh_token': _jwt.create_refresh_token(subject=user.username,
                expires_time=config_auth.JWT_R_EX_S)}

        config_auth.active_refresh_tokens.sadd(_user.uuid,
            _jwt.get_raw_jwt(tokens["refresh_token"])["jti"])
        return tokens


    def refresh_token(self, _jwt) -> dict:
        _jwt.jwt_refresh_token_required()
        _user = self.get_user(_jwt.get_jwt_subject())

        config_auth.active_refresh_tokens.srem(_user.uuid, _jwt.get_raw_jwt()["jti"])
        tokens = {"access_token": _jwt.create_access_token(subject=_user.username,
                expires_time=config_auth.JWT_A_EX_S),
                "refresh_token": _jwt.create_refresh_token(subject=_user.username,
                expires_time=config_auth.JWT_R_EX_S)}
                
        config_auth.active_refresh_tokens.sadd(_user.uuid,
            _jwt.get_raw_jwt(tokens["refresh_token"])["jti"])
        return tokens

    def user_info(self, _jwt) -> dict:
        _jwt.jwt_required()
        return {"user": UserMe.from_orm(
            self.get_user(_jwt.get_jwt_subject())
        )}

    def user_modify(self, _jwt, user: UserEmail) -> dict:
        _jwt.jwt_required()
        _user = self.get_user(_jwt.get_jwt_subject())
        if not _user:
            return {"error": "User exists"}
        for key, value in user.dict().items():
            setattr(_user, key, value)

        self.session.add(_user)
        self.session.commit()
        self.session.refresh(_user)
        config_auth.blocked_access_tokens.setex(_jwt.get_raw_jwt()["jti"],
            config_auth.JWT_A_EX_S, "true"
        )
        return {"user": UserMe.from_orm(_user),
            "access_token": _jwt.create_access_token(subject=user.username,
            expires_time=config_auth.JWT_A_EX_S)
        }

    def get_user_by_access_token(self, _jwt):
        _jwt.jwt_required()
        _username = _jwt.get_jwt_subject()
        return _username if _username else None

    def logout(self, _jwt):
        _jwt.jwt_refresh_token_required()
        _user = self.get_user(_jwt.get_jwt_subject())
        config_auth.active_refresh_tokens.srem(_user.uuid, _jwt.get_raw_jwt()["jti"])
        return {"msg": "You have been logged out."}

    def logout_all(self, _jwt):
        _jwt.jwt_refresh_token_required()
        _user = self.get_user(_jwt.get_jwt_subject())
        config_auth.active_refresh_tokens.delete(_user.uuid)
        return {"msg": "You have been logged out from all devices."}


@lru_cache()
def get_user_service(
    cache: AbstractCache = Depends(get_cache),
    session: Session = Depends(get_session),
) -> UserService:
    return UserService(cache=cache, session=session)