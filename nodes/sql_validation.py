from states.analyst_state import AnalystState
from agents.sql_agent import SQLTools
from config.llm import llm

FORBIDDEN_KEYWORDS = {
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "REPLACE"
}


def sql_review_node(state: AnalystState):
    try:
        query = state["sql_query"].strip()

        if not query:
            return {
                "query_valid": False,
                "validation_error": "Generated SQL is empty."
            }

        upper_query = query.upper()

        for keyword in FORBIDDEN_KEYWORDS:
            if keyword in upper_query:
                return {
                    "query_valid": False,
                    "validation_error": f"Forbidden SQL operation: {keyword}"
                }

        tools = SQLTools(database=state["database"], llm=llm)
        reviewed_query = tools.checker_tool.invoke(query)

        return {
            "query_valid": True,
            "reviewed_query": reviewed_query,
            "validation_error": None
        }

    except Exception as e:
        return {
            "query_valid": False,
            "validation_error": str(e)
        }