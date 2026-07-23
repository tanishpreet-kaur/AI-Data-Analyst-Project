import pandas as pd
from states.analyst_state import AnalystState

def sql_execution_node(state: AnalystState):
    try:
        query = state["reviewed_sql"]
        engine = state["database"]._engine
        df = pd.read_sql(query, engine)
        return {
            "query_result": df,
            "error": None,
        }

    except Exception as e:
        print("SQL Execution Error:", e)
        raise