from typing import TypedDict, Optional, Any

from database.context import DatabaseContext
from langchain_community.utilities import SQLDatabase


class AnalystState(TypedDict):

    # User Input
    question: str

    # Database
    database: SQLDatabase
    database_context: DatabaseContext

    # Generated SQL
    sql_query: Optional[str]

    # Query Validation
    reviewed_query: Optional[str]
    query_valid: bool
    validation_error: Optional[str]

    # Query Result
    query_result: Optional[Any]

    # Business Answer
    answer: Optional[str]