import logging
from flask_dotenv import DotEnv
dotenv = DotEnv()

class Config:
    FLASK_APP = 'server.py'
    FLASK_LOG_TYPE = 'console'

    # flask-sqlalchemy config
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/emaildb"
    SQLALCHEMY_DATABASE_URI_TEST = "postgresql://postgres:postgres@localhost/emaildb_test"
    SQLALCHEMY_ECHO = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_POOL_SIZE = 30
    SQLALCHEMY_MAX_OVERFLOW = 10
    SQLALCHEMY_POOL_TIMEOUT = 15
    SQLALCHEMY_POOL_RECYCLE = 900
    SQLALCHEMY_POOL_PRE_PING = True

    # celery config
    CELERY_TIMEZONE = "Asia/Singapore"
    CELERY_BROKER_URL = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND = "redis://localhost:6379/0"
    CELERY_SEND_SENT_EVENT = True
    CELERY_LOG_TYPE = "console"

    # flask-mail config
    MAIL_SERVER = "smtp.hostinger.com"
    MAIL_PORT = 587
    MAIL_USERNAME = "test@itmentorapps.com"
    MAIL_PASSWORD = "aj$Tr8:*1T"
    MAIL_DEFAULT_SENDER = "test@itmentorapps.com"
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False


class ProductionConfig(Config):
    ENV = 'production'
    DEVELOPMENT = False
    DEBUG = False
    LOG_LEVEL = logging.DEBUG


class StagingConfig(Config):
    ENV = 'staging'
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = logging.INFO


class DevConfig(Config):
    ENV = 'development'
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = logging.DEBUG

class TestConfig(Config):
    ENV = 'test'
    DEVELOPMENT = True
    DEBUG = True
    LOG_LEVEL = logging.DEBUG
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:postgres@localhost/emaildb_test"


app_settings = dict(
    production=ProductionConfig,
    staging=StagingConfig,
    development=DevConfig,
    testing=TestConfig,
)