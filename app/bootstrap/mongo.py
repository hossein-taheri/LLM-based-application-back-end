import os
import mongoengine as me
from dotenv import load_dotenv


def init_mongo():
    db_name = os.getenv("MONGO_DB_NAME")
    db_host = os.getenv("MONGO_DB_HOST", "localhost")
    db_port = int(os.getenv("MONGO_DB_PORT", 27017))
    db_user = os.getenv("MONGO_DB_USER")
    db_password = os.getenv("MONGO_DB_PASSWORD")

    if db_user and db_password:
        mongo_uri = f"mongodb://{db_user}:{db_password}@{db_host}:{db_port}"
    else:
        mongo_uri = f"mongodb://{db_host}:{db_port}"

    me.connect(db_name, host=mongo_uri)


load_dotenv()
init_mongo()
