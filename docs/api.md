# API Reference

Base URL for local development:

```text
http://127.0.0.1:8000
```

## GET /health

Returns backend status and current number of cached questions.

### Example response

```json
{
  "status": "ok",
  "cached_questions": 8
}
```

## POST /ask

Converts a natural-language question into SQL, runs it against MySQL, and returns a business answer.

### Request

```json
{
  "question": "Show revenue by city"
}
```

### Response

```json
{
  "question": "Show revenue by city",
  "summary": "The top result is Bengaluru with total revenue of ₹89,000.",
  "sql": "SELECT ...",
  "columns": ["city", "total_revenue"],
  "rows": [
    {
      "city": "Bengaluru",
      "total_revenue": 89000
    }
  ],
  "cache_hit": true
}
```

## Error responses

### 400 blank question

```json
{
  "detail": "Question cannot be blank."
}
```

### 400 unsafe SQL

```json
{
  "detail": "Unsafe SQL blocked. Only SELECT queries are allowed."
}
```

### 429 Gemini quota

```json
{
  "detail": "Gemini quota limit reached. Please wait and try again."
}
```
