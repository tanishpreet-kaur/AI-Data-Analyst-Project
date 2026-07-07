from dataclasses import dataclass

@dataclass
class DatabaseContext:
    database_type: str
    connection_uri: str
    schema: dict
    table_names: list[str]