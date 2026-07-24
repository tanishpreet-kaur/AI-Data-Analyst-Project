from typing import TypedDict, Optional, Any
from states.chart import VisualisationOutput
from database.context import DatabaseContext
from langchain_community.utilities import SQLDatabase

class AnalystState(TypedDict):
    question: str
    database: SQLDatabase
    database_context: DatabaseContext
    reviewed_sql: str
    review_status: str
    review_reason: str
    review_count: int
    sql_query: Optional[str]
    query_result: Optional[Any]
    answer: Optional[str]
    chart_spec: VisualisationOutput | None