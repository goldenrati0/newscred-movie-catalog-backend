import os
from datetime import timedelta
from typing import Dict, Any

from src.utils import Generator


class FlaskConfig:
    APPLICATION_ROOT: str = "/api"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "DEV")
    SECRET_KEY: str = os.getenv("SECRET_KEY", Generator.random_string_generator(length=100, punctuation=False))


class Database:
    _database: str = os.getenv("DB", "postgresql")
    _db_driver: str = os.getenv("DB_DRIVER", "psycopg2")
    _db_host: str = os.getenv("DB_HOST", "127.0.0.1")
    _db_port: int = int(os.getenv("DB_PORT", "5432"))
    _db_username: str = os.getenv("DB_USER", "postgres")
    _db_password: str = os.getenv("DB_PASSWORD", "letsplay")
    _db_name: str = os.getenv("DB_NAME", "omdb_personal")


class SQLAlchemyConfig:
    track_modifications: bool = False
    database_uri: str = f"{Database._database}+{Database._db_driver}://{Database._db_username}:{Database._db_password}@{Database._db_host}:{Database._db_port}/{Database._db_name}"
    echo: bool = False
    native_unicode: str = "utf-8"
    commit_on_teardown: bool = False
    pool_size: int = 125
    pool_recycle: int = 30
    engine_options: Dict[str, Any] = {
        "max_overflow": 50,
        "pool_pre_ping": True
    }


class RedisConfig:
    _redis_host = os.getenv("REDIS_HOST", "127.0.0.1")
    _redis_port = int(os.getenv("REDIS_PORT", "6379"))
    _redis_password = os.getenv("REDIS_PASSWORD", "")
    _redis_default_exp_time = int(os.getenv("REDIS_DEFAULT_EXPIRATION_TIME", "60"))
    _default_db_num = int(os.getenv("DEFAULT_DB_NUM", "1"))
    _flask_caching_db_num = int(os.getenv("FLASK_CACHING_DB_NUM", "0"))
    _flask_limiter_db_num = int(os.getenv("LIMITER_CACHING_DB_NUM", "5"))


class FlaskJWTExtendedConfig:
    JWT_TOKEN_LOCATION: str = ("headers", "query_string")
    JWT_HEADER_NAME: str = "Authorization"
    JWT_HEADER_TYPE: str = "Bearer"
    JWT_QUERY_STRING_NAME: str = "token"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(weeks=4)
    JWT_ALGORITHM: str = "HS512"
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY", "s3cr3t_key_change_it")
    JWT_BLACKLIST_ENABLED: bool = False


class FlaskCachingConfig:
    _cache_redis_url: str = f"redis://:{RedisConfig._redis_password}@{RedisConfig._redis_host}:{RedisConfig._redis_port}/{RedisConfig._flask_caching_db_num}"


class FlaskLimiterConfig:
    _redis_storage_url: str = f"redis://:{RedisConfig._redis_password}@{RedisConfig._redis_host}:{RedisConfig._redis_port}/{RedisConfig._flask_limiter_db_num}"


class OMDBClientConfig:
    api_key: str = os.getenv("OMDB_API_KEY", "")


class Configuration:
    # application config
    APPLICATION_ROOT: str = FlaskConfig.APPLICATION_ROOT
    ENV: str = FlaskConfig.ENVIRONMENT
    DEBUG: bool = FlaskConfig.ENVIRONMENT == "DEV"
    SECRET_KEY: str = FlaskConfig.SECRET_KEY

    # sqlalchemy config
    SQLALCHEMY_DATABASE_URI: str = SQLAlchemyConfig.database_uri
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = SQLAlchemyConfig.track_modifications
    SQLALCHEMY_ECHO: bool = SQLAlchemyConfig.echo
    SQLALCHEMY_COMMIT_ON_TEARDOWN: bool = SQLAlchemyConfig.commit_on_teardown
    SQLALCHEMY_NATIVE_UNICODE: str = SQLAlchemyConfig.native_unicode
    SQLALCHEMY_POOL_SIZE: int = SQLAlchemyConfig.pool_size
    SQLALCHEMY_POOL_RECYCLE: int = SQLAlchemyConfig.pool_recycle
    SQLALCHEMY_ENGINE_OPTIONS: Dict[str, Any] = SQLAlchemyConfig.engine_options

    # caching config
    CACHE_REDIS_URL: str = FlaskCachingConfig._cache_redis_url

    # limiter config
    LIMITER_STORAGE_URI: str = FlaskLimiterConfig._redis_storage_url

    # redis config
    REDIS_HOST = RedisConfig._redis_host
    REDIS_PORT = RedisConfig._redis_port
    REDIS_PASSWORD = RedisConfig._redis_password
    REDIS_DEFAULT_EXPIRATION_TIME = RedisConfig._redis_default_exp_time
    REDIS_DB = RedisConfig._default_db_num

    # omdb config
    OMDB_API_KEY: str = OMDBClientConfig.api_key

    # jwt token config
    JWT_TOKEN_LOCATION = FlaskJWTExtendedConfig.JWT_TOKEN_LOCATION
    JWT_HEADER_NAME = FlaskJWTExtendedConfig.JWT_HEADER_NAME
    JWT_HEADER_TYPE = FlaskJWTExtendedConfig.JWT_HEADER_TYPE
    JWT_QUERY_STRING_NAME = FlaskJWTExtendedConfig.JWT_QUERY_STRING_NAME
    JWT_ACCESS_TOKEN_EXPIRES = FlaskJWTExtendedConfig.JWT_ACCESS_TOKEN_EXPIRES
    JWT_REFRESH_TOKEN_EXPIRES = FlaskJWTExtendedConfig.JWT_REFRESH_TOKEN_EXPIRES
    JWT_ALGORITHM = FlaskJWTExtendedConfig.JWT_ALGORITHM
    JWT_SECRET_KEY = FlaskJWTExtendedConfig.JWT_SECRET_KEY
    JWT_BLACKLIST_ENABLED = FlaskJWTExtendedConfig.JWT_BLACKLIST_ENABLED
