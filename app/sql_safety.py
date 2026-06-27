import re

BLOCKED_KEYWORDS = [
    "drop",
    "delete",
    "update",
    "insert",
    "alter",
    "truncate",
    "create",
    "replace",
    "grant",
    "revoke",
    "commit",
    "rollback",
]


def clean_sql(sql_text: str) -> str:
    sql_text = sql_text.strip()
    sql_text = re.sub(r"```sql", "", sql_text, flags=re.IGNORECASE)
    sql_text = re.sub(r"```", "", sql_text)
    return sql_text.strip()


def is_safe_select_query(sql: str) -> bool:
    sql_lower = sql.lower().strip()
    if not sql_lower.startswith("select"):
        return False

    for keyword in BLOCKED_KEYWORDS:
        pattern = r"\b" + re.escape(keyword) + r"\b"
        if re.search(pattern, sql_lower):
            return False

    return True
