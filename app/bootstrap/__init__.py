from dotenv import load_dotenv

from app.bootstrap.mongo import init_mongo
from app.bootstrap.open_ai import load_open_ai_key

load_dotenv()
init_mongo()
load_open_ai_key()
