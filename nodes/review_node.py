from states.analyst_state import AnalystState
from guardrails.security import check_empty_sql, check_read_only, check_multiple_statements, check_dangerous_keywords, check_sql_injection
from guardrails.schema import validate_tables, validate_columns, validate_syntax
from guardrails.performance import add_limit_if_needed, detect_cartesian_product


def review_sql(state: AnalystState):

    sql = state["sql_query"]
    db = state["database"]
    context = state["database_context"]
    schema = context.schema

    checks = [
        check_empty_sql(sql),
        check_read_only(sql),
        check_multiple_statements(sql),
        check_dangerous_keywords(sql),
        check_sql_injection(sql),
        validate_tables(sql, schema),
        validate_columns(sql, schema),
        validate_syntax(sql, db),
        detect_cartesian_product(sql),
    ]

    for result in checks:

        if not result["passed"]:

            return {
                    **state,
                    "retry_count": state.get("retry_count", 0) + 1,
                    "review_status": "FAIL",
                    "review_reason": result["reason"]
                }

    sql = add_limit_if_needed(sql)

    return {
            **state,
            "reviewed_sql": sql,
            "retry_count": 0,
            "review_status": "PASS",
            "review_reason": "SQL validated."
        }