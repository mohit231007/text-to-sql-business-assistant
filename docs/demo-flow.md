# Demo Flow

This note gives a simple, non-runtime walkthrough for presenting the Text-to-SQL Business Assistant as a portfolio project.

## Suggested walkthrough

1. Start the FastAPI backend.
2. Start the Streamlit frontend.
3. Ask a simple revenue question.
4. Ask a product or customer ranking question.
5. Review the table output and the plain-English summary.
6. Explain how the same architecture can support a real analytics dataset through a controlled database connection.

## Talking points

- The project shows how natural-language analytics can reduce dependency on manual report building.
- The backend separates application logic, model calls, database access, and summarisation.
- The frontend keeps the workflow simple for a non-technical stakeholder.
- The sample dataset makes the project easy to test locally without touching production data.

## Maintenance note

Keep documentation and examples aligned with the codebase whenever the API, frontend, or database schema changes.
