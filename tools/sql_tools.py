from langchain_community.agent_toolkits.sql.toolkit import SQLDatabaseToolkit

from langchain_community.tools.sql_database.tool import (
    QuerySQLDatabaseTool,
    QuerySQLCheckerTool,
    InfoSQLDatabaseTool,
    ListSQLDatabaseTool,
)


class SQLTools:

    def __init__(self, database, llm):

        toolkit = SQLDatabaseToolkit(
            db=database,
            llm=llm,
        )

        self.toolkit = toolkit

        self.tools = {
            tool.name: tool
            for tool in toolkit.get_tools()
        }

        self.query_tool: QuerySQLDatabaseTool = self.tools[
            "sql_db_query"
        ]

        self.checker_tool: QuerySQLCheckerTool = self.tools[
            "sql_db_query_checker"
        ]

        self.schema_tool: InfoSQLDatabaseTool = self.tools[
            "sql_db_schema"
        ]

        self.table_tool: ListSQLDatabaseTool = self.tools[
            "sql_db_list_tables"
        ]