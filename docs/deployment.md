# Deployment Notes

## Local development

Run the backend:

```bash
uvicorn app.main:app --reload --port 8000
```

Run the frontend:

```bash
streamlit run frontend/streamlit_app.py
```

## Backend deployment

You can deploy the FastAPI backend to:

- Render
- Railway
- Fly.io
- Azure App Service
- AWS App Runner

Set environment variables on the backend host:

```env
GOOGLE_API_KEY=...
DB_USER=readonly_user
DB_PASSWORD=...
DB_HOST=...
DB_PORT=3306
DB_NAME=text_to_sql
ALLOWED_ORIGINS=https://your-frontend-domain.com
```

## Database security

Do not use `root` in production.

Create a read-only MySQL user:

```sql
CREATE USER 'textsql_reader'@'%' IDENTIFIED BY 'strong_password_here';
GRANT SELECT ON text_to_sql.* TO 'textsql_reader'@'%';
FLUSH PRIVILEGES;
```

## Frontend deployment

Streamlit can be deployed to Streamlit Community Cloud or any Python-friendly hosting platform.

Set:

```env
TEXT_TO_SQL_API_URL=https://your-fastapi-backend.com
```

## Production hardening checklist

- Use HTTPS only
- Use a read-only database user
- Restrict CORS
- Add authentication
- Add rate limiting
- Add request logging
- Add audit logs for generated SQL
- Replace in-memory cache with Redis for multi-instance deployment
