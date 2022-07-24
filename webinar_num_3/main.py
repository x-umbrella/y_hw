import redis
import uvicorn
from fastapi import FastAPI

from src.api.v1.resources import posts, users, users_me
from src.core import config, config_auth
from src.db import cache, redis_cache, init_db

app = FastAPI(
    # Конфигурируем название проекта. Оно будет отображаться в документации
    title=config.PROJECT_NAME,      
    version=config.VERSION,
    # Адрес документации в красивом интерфейсе
    docs_url="/api/openapi",
    redoc_url="/api/redoc",
    # Адрес документации в формате OpenAPI
    openapi_url="/api/openapi.json",
)


@app.on_event("startup")
def startup():
    """Подключаемся к базам при старте сервера"""
    init_db()
    cache.cache = redis_cache.CacheRedis(
        cache_instance=redis.Redis(
            host=config.REDIS_HOST, port=config.REDIS_PORT, max_connections=10
        )
    )


@app.on_event("shutdown")
def shutdown():
    """Отключаемся от баз при выключении сервера"""
    cache.cache.close()
    config_auth.active_refresh_tokens.close()
    config_auth.blocked_access_tokens.close()


# Подключаем роутеры к серверу
app.include_router(router=users.router, prefix="/api/v1")
app.include_router(router=users_me.router, prefix="/api/v1/users/me")

@app.get("/")
def root():
    return {"service": config.PROJECT_NAME, "version": config.VERSION}

app.include_router(router=posts.router, prefix="/api/v1/posts")


if __name__ == "__main__":
    # Приложение может запускаться командой
    # `uvicorn main:app --host 0.0.0.0 --port 8000`
    # но чтобы не терять возможность использовать дебагер,
    # запустим uvicorn сервер через python
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
    )
