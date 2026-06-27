from typing import Any

import pandas as pd
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.config import get_settings
from app.database import get_engine
from app.llm import get_llm
from app.schema_reader import get_schema
from app.sql_cache import cache_size, get_cached_sql, set_cached_sql
from app.sql_safety import clean_sql, is_safe_select_query
from app.summary import generate_business_summary

settings = get_settings()
engine = get_engine()
llm = get_llm()

app = FastAPI(title="Text-to-SQL Business Assistant API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AskRequest(BaseModel):
    question: str


class AskResponse(BaseModel):
    question: str
    summary: str
    sql: str
    columns: list[str]
    rows: list[dict[str, Any]]
    cache_hit: bool = False


def generate_sql(question: str) -> tuple[str, bool]:
    cached_sql = get_cached_sql(question)
    if cached_sql:
        return cached_sql, True

    schema = get_schema(engine)

    prompt = f"""
You are an expert MySQL business analyst.

Convert the user's business question into one valid MySQL SELECT query.

Rules:
1. Return only SQL.
2. Do not explain.
3. Do not use markdown.
4. Use only the tables and columns shown in the schema.
5. Never generate INSERT, UPDATE, DELETE, DROP, ALTER, CREATE, TRUNCATE, GRANT, REVOKE, COMMIT, or ROLLBACK.
6. If revenue is asked, calculate it as:
   SUM(order_items.quantity * products.price)
7. When ranking by revenue, include the revenue value in the SELECT output.
8. When ranking by quantity, include total quantity in the SELECT output.
9. Use clear aliases such as total_revenue, total_orders, total_units_sold.
10. Prefer business-readable outputs such as customer_name, city, category, product_name, order_date.
11. If a LIMIT is useful for top, highest, lowest, most, or least questions, use LIMIT.
12. Generate MySQL-compatible SQL only.

Database schema:
{schema}

User question:
{question}
"""

    response = llm.invoke(prompt)
    sql = clean_sql(response.content)
    set_cached_sql(question, sql)
    return sql, False


@app.get("/health")
def health():
    return {"status": "ok", "cached_questions": cache_size()}


@app.post("/ask", response_model=AskResponse)
def ask(payload: AskRequest):
    question = payload.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be blank.")

    try:
        sql, cache_hit = generate_sql(question)

        if not is_safe_select_query(sql):
            raise HTTPException(status_code=400, detail="Unsafe SQL blocked. Only SELECT queries are allowed.")

        result_df = pd.read_sql(sql, engine)
        summary = generate_business_summary(question, result_df)
        result_df = result_df.where(pd.notnull(result_df), None)

        return {
            "question": question,
            "summary": summary,
            "sql": sql,
            "columns": result_df.columns.tolist(),
            "rows": result_df.to_dict(orient="records"),
            "cache_hit": cache_hit,
        }

    except HTTPException:
        raise
    except Exception as e:
        error_text = str(e)
        if "RESOURCE_EXHAUSTED" in error_text or "429" in error_text:
            raise HTTPException(status_code=429, detail="Gemini quota limit reached. Please wait and try again.")
        raise HTTPException(status_code=500, detail=error_text)
