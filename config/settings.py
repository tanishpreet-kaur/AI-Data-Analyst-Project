from dotenv import load_dotenv
import os

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

UPLOAD_FOLDER = "uploads"
SQLITE_PREFIX = "sqlite:///"
POSTGRES_PREFIX = "postgresql+psycopg2://"
MYSQL_PREFIX = "mysql+pymysql://"