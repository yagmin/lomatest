import os

from sqlalchemy.engine.url import URL


class Configuration(object):
    ###################################
    # FLASK CONFIG
    SECRET_KEY = "Yjlaskdffdasdfsfdfjloiasdfh"

    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")

    JSON_SORT_KEYS = False

    ###################################
    # FLASK-SQLALCHEMY CONFIG
    SQLALCHEMY_DATABASE_URI = URL.create(
        "postgresql",
        username="postgres",
        password="",
        host="localhost",
        port=5432,
        database="lomatest",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECORD_QUERIES = False
