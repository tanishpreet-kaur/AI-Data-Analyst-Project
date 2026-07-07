from pathlib import Path
from langchain_community.utilities import SQLDatabase
from utils.logger import logger

class DatabaseManager:
    """
    Handles creation and validation of LangChain SQLDatabase objects.
    Supports SQLite, PostgreSQL and MySQL.
    """

    def __init__(self):
        self.database = None
        self.connection_uri = None

    def create_database(self, database_type: str, **kwargs) -> SQLDatabase:
        """
        Creates a SQLDatabase instance based on the database type.
        """

        if database_type == "sqlite":
            uri = self._build_sqlite_uri(kwargs["path"])

        elif database_type == "postgres":
            uri = self._build_postgres_uri(
                username=kwargs["username"],
                password=kwargs["password"],
                host=kwargs["host"],
                port=kwargs["port"],
                database=kwargs["database"],
            )

        elif database_type == "mysql":
            uri = self._build_mysql_uri(
                username=kwargs["username"],
                password=kwargs["password"],
                host=kwargs["host"],
                port=kwargs["port"],
                database=kwargs["database"],
            )

        else:
            raise ValueError(f"Unsupported database type: {database_type}")

        logger.info(f"Connecting to {database_type} database")
        self.connection_uri = uri

        try:
            self.database = SQLDatabase.from_uri(uri)
            self._validate_connection()
            logger.info("Database connection successful.")
            return self.database

        except Exception as e:
            logger.exception("Database connection failed.")
            raise ConnectionError(
                f"Failed to connect to database.\n{str(e)}"
            )

    def get_database(self) -> SQLDatabase:
        if self.database is None:
            raise RuntimeError("Database has not been initialized.")
        return self.database

    @staticmethod
    def _build_sqlite_uri(path):
        return f"sqlite:///{Path(path)}"

    @staticmethod
    def _build_postgres_uri(username, password, host, port, database,):
        return (
            f"postgresql+psycopg2://"
            f"{username}:{password}@"
            f"{host}:{port}/{database}"
        )

    @staticmethod
    def _build_mysql_uri(username, password, host, port, database,):
        return (
            f"mysql+pymysql://"
            f"{username}:{password}@"
            f"{host}:{port}/{database}"
        )

    def _validate_connection(self):
        try:
            tables = self.database.get_usable_table_names()
            logger.info(
                f"Connection validated. Found {len(tables)} tables."
            )

        except Exception as e:
            logger.exception("Validation failed.")
            raise RuntimeError(str(e))