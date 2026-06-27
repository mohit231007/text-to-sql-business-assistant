# Text-to-SQL Business Assistant

A public, reusable **Text-to-SQL business analytics assistant** built with **FastAPI, Gemini, LangChain, MySQL, SQLAlchemy and Streamlit**.

The app lets non-technical users ask business questions in plain English, generates safe MySQL `SELECT` queries, executes them against a relational database, and returns a client-friendly summary, result table and downloadable output.

> Example: `Show revenue by city` → SQL → MySQL result → business summary + table.

---

## Features

- Plain-English business questions
- Gemini + LangChain Text-to-SQL generation
- MySQL execution through SQLAlchemy
- Read-only SQL guardrails: only `SELECT` queries are allowed
- In-memory SQL cache so repeated questions do **not** call Gemini again
- Pre-seeded SQL for common sample questions
- Quota-friendly Python-generated summaries
- FastAPI backend with `/ask` and `/health`
- Streamlit frontend for non-technical users
- Sample database schema and seed data
- Deployment notes for public demos

---

## Architecture

```text
User question
   ↓
Streamlit frontend or API client
   ↓
FastAPI /ask endpoint
   ↓
SQL cache lookup
   ↓ cache miss
Gemini + LangChain generates MySQL SELECT query
   ↓
SQL safety check
   ↓
MySQL execution
   ↓
Business summary + table + rows
```

---

## Project structure

```text
text-to-sql-business-assistant/
├─ app/
│  ├─ main.py
│  ├─ config.py
│  ├─ database.py
│  ├─ llm.py
│  ├─ schema_reader.py
│  ├─ sql_cache.py
│  ├─ sql_safety.py
│  └─ summary.py
├─ frontend/
│  └─ streamlit_app.py
├─ sql/
│  ├─ 01_create_database.sql
│  ├─ 02_create_tables.sql
│  ├─ 03_insert_sample_data.sql
│  └─ 04_validation_queries.sql
├─ docs/
│  ├─ architecture.md
│  ├─ api.md
│  └─ deployment.md
├─ examples/
│  └─ sample_questions.md
├─ .env.example
├─ .gitignore
├─ LICENSE
└─ requirements.txt
```

---

## Quick start

### 1. Clone the repo

```bash
git clone https://github.com/mohit231007/text-to-sql-business-assistant.git
cd text-to-sql-business-assistant
```

### 2. Create a virtual environment

```bash
python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate
```

### 3. Install packages

```bash
pip install -r requirements.txt
```

### 4. Create MySQL database and sample data

Run these scripts in MySQL Workbench or MySQL CLI:

```text
sql/01_create_database.sql
sql/02_create_tables.sql
sql/03_insert_sample_data.sql
sql/04_validation_queries.sql
```

### 5. Configure environment variables

Copy `.env.example` to `.env`:

```bash
cp .env.example .env
```

On Windows CMD:

```bat
copy .env.example .env
```

Update `.env` with your values:

```env
GOOGLE_API_KEY=your_google_gemini_api_key
DB_USER=root
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=text_to_sql
ALLOWED_ORIGINS=http://localhost:8501,http://localhost:8000,http://localhost:5173,http://localhost:8080
```

---

## Run FastAPI backend

```bash
uvicorn app.main:app --reload --port 8000
```

Open:

```text
http://127.0.0.1:8000/health
http://127.0.0.1:8000/docs
```

Test `/ask` with:

```json
{
  "question": "Show revenue by city"
}
```

---

## Run Streamlit frontend

In another terminal:

```bash
streamlit run frontend/streamlit_app.py
```

Open:

```text
http://localhost:8501
```

---

## Example questions

- Show revenue by city
- Which customer generated the highest revenue?
- Which product sold the most units?
- Show category wise revenue
- How many orders did each customer place?
- Show total revenue by customer
- What products did Mohit Bhatnagar buy?

---

## SQL cache behavior

The backend uses a cache-first strategy:

1. Normalize the user's question.
2. Check whether SQL already exists in memory.
3. If found, skip Gemini and run cached SQL.
4. If not found, call Gemini once, validate the SQL, cache it, and run it.

This helps avoid repeated Gemini calls and reduces quota usage.

---

## Safety guardrails

The app blocks destructive SQL keywords such as:

```text
DROP, DELETE, UPDATE, INSERT, ALTER, TRUNCATE, CREATE, REPLACE, GRANT, REVOKE, COMMIT, ROLLBACK
```

Only queries starting with `SELECT` are allowed.

For production, also use a **read-only MySQL user**.

---

## Production notes

For a public deployment:

- Deploy FastAPI to Render, Railway, Fly.io, Azure App Service or AWS App Runner.
- Keep `.env` secrets only on the backend host.
- Use a read-only database user.
- Restrict CORS to your frontend domain.
- Add authentication or rate limiting before exposing sensitive data.
- Consider a persistent cache such as Redis for production.

---

## License

MIT License. See `LICENSE`.
