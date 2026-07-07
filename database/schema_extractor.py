from langchain_community.utilities import SQLDatabase
from utils.logger import logger

class SchemaExtractor:
    def __init__(self, database: SQLDatabase):
        self.db = database

    def extract(self):
        schema = {}
        logger.info("Extracting schema")
        tables = self.db.get_usable_table_names()
        for table in tables:
            schema[table] = self.db.get_table_info([table])
        logger.info(f"Extracted {len(schema)} tables")
        return schema