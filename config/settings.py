from dotenv import load_dotenv
from decouple import config

load_dotenv()

OPENROUTER_API_KEY = config("OPENROUTER_API_KEY")

UPLOAD_FOLDER = "uploads"
SQLITE_PREFIX = "sqlite:///"
POSTGRES_PREFIX = "postgresql+psycopg2://"
MYSQL_PREFIX = "mysql+pymysql://"