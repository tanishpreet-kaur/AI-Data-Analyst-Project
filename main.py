import streamlit as st
from database.upload_handler import save_uploaded_database
from database.database_manager import DatabaseManager
from database.schema_extractor import SchemaExtractor
from database.context import DatabaseContext
from langchain_community.utilities import SQLDatabase
import pandas as pd
import plotly.express as px
import uuid
from graph.workflow import analyst_bot

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())
    
st.set_page_config(
    page_title="AI Data Analyst",
    layout="wide",
)

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []
    
# Main Header
st.title("AI Data Analyst")
st.caption("What would you like to analyze today?")

# Side bar for uploads and chat history
with st.sidebar:
    st.title("AI Data Analyst")

    manager = DatabaseManager()

    db_type = st.selectbox(
        "Select Database",
        [
            "SQLite",
            "PostgreSQL",
            "MySQL",
        ],
    )

    def create_database_context(database_type: str, database: SQLDatabase) -> DatabaseContext:
        extractor = SchemaExtractor(database)
        schema = extractor.extract()
        tables = database.get_usable_table_names()
        context = DatabaseContext(
            database_type=database_type,
            connection_uri=manager.connection_uri,
            schema=schema,
            table_names=tables,
        )
        return context

    # SQLite
    if db_type == "SQLite":
        uploaded_db = st.file_uploader(
            "Upload SQLite Database",
            type=["db", "sqlite", "sqlite3"],
        )

        if uploaded_db:
            try:
                db_path = save_uploaded_database(uploaded_db)
                database = manager.create_database(
                    database_type="sqlite",
                    path=db_path,
                )

                context = create_database_context(db_type, database)
                st.session_state["database"] = database
                st.session_state["database_context"] = context
                st.success("SQLite database connected successfully!")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

    # PostgreSQL
    elif db_type == "PostgreSQL":
        host = st.text_input("Host", "localhost")
        port = st.text_input("Port", "5432")
        database_name = st.text_input("Database Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Connect PostgreSQL"):
            try:
                database = manager.create_database(
                    database_type="postgres",
                    username=username,
                    password=password,
                    host=host,
                    port=port,
                    database=database_name,
                )
                context = create_database_context(db_type, database)
                st.session_state["database"] = database
                st.session_state["database_context"] = context
                st.success("PostgreSQL connected successfully!")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

    # MySQL
    elif db_type == "MySQL":
        host = st.text_input("Host", "localhost")
        port = st.text_input("Port", "3306")
        database_name = st.text_input("Database Name")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Connect MySQL"):
            try:
                database = manager.create_database(
                    database_type="mysql",
                    username=username,
                    password=password,
                    host=host,
                    port=port,
                    database=database_name,
                )
                context = create_database_context(db_type, database)
                st.session_state["database"] = database
                st.session_state["database_context"] = context
                st.success("MySQL connected successfully!")
            except Exception as e:
                st.error(f"Connection Failed: {e}")

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

        if "table" in message:
            st.dataframe(message["table"])
            
if "analyst_bot" not in st.session_state:
    st.session_state["analyst_bot"] = analyst_bot

if "database" not in st.session_state:
    st.info("Please connect a database first.")
    st.stop()
    
# User Input
prompt = st.chat_input("Ask a question about your data...")

if prompt:
    # Add User Message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Assistant Response
    with st.chat_message("assistant"):
        with st.spinner("Analyzing data..."):
            
            response = analyst_bot.invoke(
                        {
                            "question": prompt,
                            "database": st.session_state["database"],
                            "database_context": st.session_state["database_context"],
                        },
                        config={
                            "configurable": {
                                "thread_id": st.session_state.thread_id
                            }
                        }
                    )

            st.markdown(response["answer"])
            
            chart = response.get("chart_spec")
            query_result = response.get("query_result")

            assistant_message = {
                "role": "assistant",
                "content": response["answer"],
                "chart_spec": chart,          
                "table": query_result,        
            }
            st.session_state.messages.append(assistant_message)

            if chart and chart.create_chart and query_result is not None:
                fig = create_plot(
                    data=query_result,
                    chart_type=chart.chart_type,
                    x_column=chart.x_column,
                    y_column=chart.y_column,
                    title=chart.title
                )
                if chart.create_chart and fig is None:
                    st.warning(f"Could not render chart type '{chart.chart_type}'.")
                elif fig:
                    st.plotly_chart(fig, use_container_width=True)
