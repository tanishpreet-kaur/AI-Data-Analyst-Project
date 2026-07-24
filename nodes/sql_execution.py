import pandas as pd
from states.analyst_state import AnalystState
import logger

def sql_execution_node(state: AnalystState):
    try:
        query = state["reviewed_sql"]
        engine = state["database"]._engine
        df = pd.read_sql(query, engine)
        return {"query_result": df, "error": None}
    
    except Exception as e:
        logger.error("SQL execution failed: %s", e)
        return {
            "query_result": None,
            "error": str(e),
            "answer": "I ran into a database error executing that query.",
            "chart_spec": None,
        }
