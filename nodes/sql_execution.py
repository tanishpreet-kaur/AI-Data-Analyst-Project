from states.analyst_state import AnalystState
from config.llm import llm
from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit


def sql_execution_node(state: AnalystState):

    try:

        toolkit = SQLDatabaseToolkit(
            db=state["database"],
            llm=llm,
        )

        tools = {
            tool.name: tool
            for tool in toolkit.get_tools()
        }

        query_tool = tools["sql_db_query"]

        query = (
            state["reviewed_query"]
            if state.get("reviewed_query")
            else state["sql_query"]
        )

        result = query_tool.invoke(query)

        return {
            "query_result": result,
            "error": None,
        }

    except Exception as e:
        print("SQL Execution Error:", e)
        raise