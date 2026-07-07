import streamlit as st
from database.upload_handler import save_uploaded_database
from database.database_manager import DatabaseManager
from database.schema_extractor import SchemaExtractor
from database.context import DatabaseContext
from langchain_community.utilities import SQLDatabase

st.set_page_config(
    page_title="AI Data Analyst",
    layout="wide",
)

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
        database_type=db_type,
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
            st.session_state["database_context"] = context
            st.success("MySQL connected successfully!")
        except Exception as e:
            st.error(f"Connection Failed: {e}")

if "database_context" in st.session_state:
    st.divider()
    st.header("Ask your database")
    question = st.chat_input("Ask anything...")

