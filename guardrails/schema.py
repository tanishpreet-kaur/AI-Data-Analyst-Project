import re

def success():
    return {"passed": True}


def failure(reason):
    return {
        "passed": False,
        "reason": reason,
    }


def validate_tables(sql, schema):
    tables = re.findall(
        r"(?:FROM|JOIN)\s+([A-Za-z_][A-Za-z0-9_]*)",
        sql,
        re.IGNORECASE,
    )
    valid = set(schema.keys())
    for table in tables:
        if table not in valid:
            return failure(f"Unknown table '{table}'.")
    return success()


def validate_columns(sql, schema):
    return success()


def validate_syntax(sql, db):
    try:

        db.run(
            f"EXPLAIN QUERY PLAN {sql}"
        )
        return success()

    except Exception as e:
        return failure(str(e))