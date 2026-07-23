from states.analyst_state import AnalystState

MAX_RETRIES = 2

def review_router(state: AnalystState):
    if state["review_status"] == "PASS":
        return "sql_executor"
    
    retries = state.get("retry_count", 0)
    
    if retries < MAX_RETRIES:
        return "sql_generator"
    return "end"

def generation_router(state):
    if state.get("review_status") == "BLOCKED":
        return "end"
    return "review_sql"