from typing import TypedDict, Optional, Any
from states.chart import ChartSpec
from database.context import DatabaseContext
from langchain_community.utilities import SQLDatabase


class AnalystState(TypedDict):
    question: str
    database: SQLDatabase
    database_context: DatabaseContext
    sql_query: Optional[str]
    query_result: Optional[Any]
    answer: Optional[str]
    chart_spec: ChartSpec | None