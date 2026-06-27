import pandas as pd
from sqlalchemy.engine import Engine
from app.config import get_settings


def get_schema(engine: Engine) -> str:
    settings = get_settings()
    schema_query = f"""
    SELECT
        TABLE_NAME AS table_name,
        COLUMN_NAME AS column_name,
        DATA_TYPE AS data_type
    FROM INFORMATION_SCHEMA.COLUMNS
    WHERE TABLE_SCHEMA = '{settings.db_name}'
    ORDER BY TABLE_NAME, ORDINAL_POSITION;
    """

    df = pd.read_sql(schema_query, engine)
    df.columns = [str(col).lower().strip() for col in df.columns]

    schema_text = ""
    for table_name in df["table_name"].unique():
        schema_text += f"\nTable: {table_name}\n"
        table_cols = df[df["table_name"] == table_name]
        for _, row in table_cols.iterrows():
            schema_text += f"  - {row['column_name']} ({row['data_type']})\n"

    return schema_text
