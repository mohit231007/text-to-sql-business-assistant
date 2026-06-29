# Contributing to Text-to-SQL Business Assistant

Thank you for helping improve this public Text-to-SQL business analytics assistant. The goal of this project is to make business data exploration easier for non-technical users while keeping database access safe, explainable, and demo-friendly.

## Good first contributions

Useful contributions include:

- Improving documentation, examples, and setup steps.
- Adding more sample business questions in `examples/sample_questions.md`.
- Strengthening SQL safety checks so only read-only queries are executed.
- Adding tests for SQL validation, caching, API responses, and error handling.
- Improving Streamlit user experience for non-technical users.
- Adding deployment notes for common hosting platforms.

## Local setup

1. Fork or clone the repository.
2. Create and activate a Python virtual environment.
3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Copy `.env.example` to `.env` and add local development values.
5. Load the SQL scripts from the `sql/` folder into MySQL.
6. Run the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

7. Run the frontend in a second terminal:

```bash
streamlit run frontend/streamlit_app.py
```

## Development standards

Please keep changes practical, readable, and easy to review.

- Keep secrets out of commits. Never commit `.env`, API keys, database passwords, access tokens, or production credentials.
- Prefer small pull requests with one clear purpose.
- Use descriptive commit messages, such as `Add SQL validation tests` or `Improve deployment guide`.
- Keep backend changes compatible with FastAPI and SQLAlchemy.
- Keep frontend changes simple for business users who may not know SQL.
- Update documentation when behavior, setup, endpoints, or environment variables change.

## SQL safety expectations

This project should remain read-only by default.

Contributions that touch SQL generation or execution should preserve these expectations:

- Only `SELECT` queries should be allowed.
- Destructive keywords such as `DROP`, `DELETE`, `UPDATE`, `INSERT`, `ALTER`, and `TRUNCATE` should be blocked.
- Production deployments should use a read-only database user.
- User-facing error messages should be helpful without exposing private schema, secrets, stack traces, or credentials.

## Suggested testing checklist

Before opening a pull request, run the relevant checks locally:

```bash
python -m compileall app frontend
```

Then manually verify:

- `/health` returns a healthy response.
- `/ask` returns SQL, a business summary, and rows for a known sample question.
- Repeated common questions use the cache path where applicable.
- Unsafe SQL-like prompts are rejected.
- The Streamlit app can call the FastAPI backend successfully.

## Pull request checklist

Before submitting, confirm that:

- The change has a clear purpose.
- Documentation is updated where needed.
- No secrets or local-only files are included.
- The app still starts locally.
- The change improves safety, usability, reliability, or maintainability.

## License

By contributing, you agree that your contribution will be released under the repository's MIT License.
