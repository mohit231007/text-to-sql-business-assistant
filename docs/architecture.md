# Architecture

The project has two user-facing options:

1. **FastAPI backend** for API clients and production deployments.
2. **Streamlit frontend** for quick local demos and non-technical users.

## Flow

```text
User question
  ↓
Frontend / API client
  ↓
POST /ask
  ↓
Normalize question
  ↓
SQL cache lookup
  ↓ cache miss
Gemini + LangChain generate SQL
  ↓
SQL safety validation
  ↓
MySQL execution
  ↓
Python-generated business summary
  ↓
JSON response / UI table
```

## Why cache SQL?

Text-to-SQL systems often receive repeated questions such as:

- Show revenue by city
- Which customer generated the highest revenue?
- Show category wise revenue

The generated SQL does not need to be regenerated each time. The cache stores SQL by normalized question text, reducing cost, latency and quota pressure.

## Safety model

This project uses layered safety:

- The prompt instructs Gemini to generate only MySQL `SELECT` queries.
- The backend blocks non-`SELECT` SQL.
- The backend blocks destructive keywords.
- Production should use a read-only database user.

## Production improvements

For serious use, add:

- Redis or database-backed SQL cache
- user authentication
- rate limiting
- query audit logs
- table/column allowlists by role
- read-only DB user
- monitoring and alerts
