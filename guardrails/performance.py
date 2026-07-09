import re

def success():
    return {"passed": True}


def failure(reason):
    return {
        "passed": False,
        "reason": reason,
    }


def detect_cartesian_product(sql):
    upper = sql.upper()
    tables = re.findall(
        r"(FROM|JOIN)\s+",
        upper,
    )

    if len(tables) > 1:
        if "JOIN" not in upper and "WHERE" not in upper:
            return failure(
                "Possible Cartesian Product."
            )
    return success()


def add_limit_if_needed(sql):
    upper = sql.upper()
    if "LIMIT" in upper:
        return sql
    
    if any(
        word in upper
        for word in [
            "COUNT(",
            "SUM(",
            "AVG(",
            "MAX(",
            "MIN(",
            "GROUP BY",
        ]
    ):
        return sql
    return sql.rstrip(";") + " LIMIT 100;"