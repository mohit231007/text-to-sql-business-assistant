import os
import requests
import pandas as pd
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_URL = os.getenv("TEXT_TO_SQL_API_URL", "http://127.0.0.1:8000").rstrip("/")

st.set_page_config(
    page_title="Text-to-SQL Business Assistant",
    page_icon="📊",
    layout="wide",
)

st.title("📊 Text-to-SQL Business Assistant")
st.markdown("Ask business questions in plain English and get database-backed answers.")

example_questions = [
    "Show revenue by city",
    "Which customer generated the highest revenue?",
    "Which product sold the most units?",
    "Show category wise revenue",
    "How many orders did each customer place?",
    "Show total revenue by customer",
    "What products did Mohit Bhatnagar buy?",
]

with st.sidebar:
    st.header("Examples")
    for item in example_questions:
        if st.button(item):
            st.session_state["question"] = item

    st.divider()
    st.caption("Backend API")
    st.code(API_URL)

question = st.text_input(
    "Ask your business question:",
    value=st.session_state.get("question", "Show revenue by city"),
)

show_sql = st.checkbox("Show generated SQL", value=False)

if st.button("Ask Assistant", type="primary"):
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Asking backend..."):
            try:
                response = requests.post(
                    f"{API_URL}/ask",
                    json={"question": question.strip()},
                    timeout=60,
                )
                response.raise_for_status()
                data = response.json()

                st.subheader("Business Answer")
                st.markdown(data.get("summary", "No summary returned."))

                rows = data.get("rows", [])
                columns = data.get("columns", [])
                df = pd.DataFrame(rows, columns=columns)

                st.subheader("Result Table")
                st.dataframe(df, use_container_width=True)

                if len(df.columns) >= 2:
                    numeric_cols = df.select_dtypes(include="number").columns.tolist()
                    text_cols = df.select_dtypes(exclude="number").columns.tolist()
                    numeric_cols = [col for col in numeric_cols if "id" not in col.lower()]
                    if numeric_cols and text_cols:
                        st.subheader("Visual View")
                        st.bar_chart(df.set_index(text_cols[0])[numeric_cols[0]])

                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download CSV",
                    data=csv,
                    file_name="text_to_sql_result.csv",
                    mime="text/csv",
                )

                st.caption(f"Cache hit: {data.get('cache_hit', False)}")

                if show_sql:
                    st.subheader("Generated SQL")
                    st.code(data.get("sql", ""), language="sql")

            except requests.HTTPError as exc:
                detail = exc.response.text if exc.response is not None else str(exc)
                st.error(f"Backend returned an error: {detail}")
            except Exception as exc:
                st.error(f"Could not reach backend: {exc}")
