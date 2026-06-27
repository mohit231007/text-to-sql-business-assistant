from typing import Any
import pandas as pd


def format_metric(column_name: str, value: Any) -> str:
    if value is None:
        return "no value"

    label = column_name.replace("_", " ")

    if isinstance(value, (int, float)):
        if any(token in column_name.lower() for token in ["revenue", "spend", "price", "sales"]):
            return f"{label} of ₹{value:,.0f}"
        return f"{label} of {value:,.0f}"

    return f"{label} of {value}"


def generate_business_summary(question: str, result_df: pd.DataFrame) -> str:
    if result_df.empty:
        return "No records were found for this question."

    if len(result_df.columns) >= 2:
        first_col = result_df.columns[0]
        second_col = result_df.columns[1]
        top_row = result_df.iloc[0]
        return f"The top result is {top_row[first_col]} with {format_metric(second_col, top_row[second_col])}."

    return f"The query returned {len(result_df)} matching record(s) from the database."
