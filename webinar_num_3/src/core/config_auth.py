
import redis
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from .config import (
    JWT_A_EX_S,
    JWT_R_EX_S,
    JWT_SECRET_KEY,
    REDIS_HOST,
    REDIS_PORT
)


class Settings(BaseModel):
    access_expires: int = JWT_A_EX_S
    refresh_expires: int = JWT_R_EX_S
    authjwt_secret_key = JWT_SECRET_KEY
    host = REDIS_HOST
    port = REDIS_PORT
    authjwt_denylist_token_checks: set = {'access', 'refresh'}
    authjwt_denylist_enabled: bool = True
    


settings = Settings()


active_refresh_tokens = redis.Redis(
    host=settings.host,
    port=settings.port,
    db=2,
    decode_responses=True,
)
blocked_access_tokens = redis.Redis(
    host=settings.host,
    port=settings.port,
    db=1,
    decode_responses=True,
)


@AuthJWT.load_config
def get_config():
    return Settings()


@AuthJWT.token_in_denylist_loader
def check_if_token_in_denylist(decrypted_token):
    jti = decrypted_token['jti']
    entry = blocked_access_tokens.get(jti)
    return entry and entry == 'true'




