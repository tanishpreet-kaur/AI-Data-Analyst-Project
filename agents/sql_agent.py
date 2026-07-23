from langchain.agents import create_agent
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit
from config.llm import llm
from prompts.sql_prompt import SQL_PROMPT

def create_sql_agent(database):
    toolkit = SQLDatabaseToolkit(
        db=database,
        llm=llm
    )

    read_only_tools = [
        tool for tool in toolkit.get_tools()
        if tool.name != "sql_db_query"
    ]

    return create_agent(
        model=llm,
        tools=read_only_tools,
        system_prompt=SQL_PROMPT
    )