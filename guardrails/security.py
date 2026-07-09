import sqlparse

DANGEROUS = {
    "DROP",
    "DELETE",
    "UPDATE",
    "INSERT",
    "ALTER",
    "TRUNCATE",
    "CREATE",
    "ATTACH",
    "DETACH",
    "VACUUM",
    "PRAGMA",
    "REPLACE",
}


def success():
    return {"passed": True}


def failure(reason):
    return {
        "passed": False,
        "reason": reason,
    }


def check_empty_sql(sql):
    if sql is None or sql.strip() == "":
        return failure("Empty SQL generated.")
    return success()


def check_read_only(sql):
    first = sql.strip().split()[0].upper()
    if first not in ["SELECT", "WITH"]:
        return failure("Only SELECT statements are allowed.")
    return success()


def check_multiple_statements(sql):
    if len(sqlparse.split(sql)) > 1:
        return failure("Multiple SQL statements detected.")
    return success()


def check_dangerous_keywords(sql):
    upper = sql.upper()
    for word in DANGEROUS:
        if word in upper:
            return failure(f"Dangerous keyword '{word}' detected.")
    return success()


def check_sql_injection(sql):
    sql = sql.upper()
    patterns = [
        "--",
        "/*",
        "*/",
        " OR 1=1",
        "UNION SELECT",
        "XP_",
        "EXEC",
    ]
    for p in patterns:
        if p in sql:
            return failure("Possible SQL Injection detected.")
    return success()