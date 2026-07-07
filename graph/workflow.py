from langgraph.graph import StateGraph, START, END
from states.SQLAgentState import SQLAgentState
from nodes.sql_creation import create_generate_sql_node
from nodes.review_node import review_sql, route_after_review
from nodes.execute_sql import create_execute_and_generate_insights_node
from nodes.visualisation_node import visualisation_node
from utils.sql_utils import create_sql_tools
from model.llm import llm
from agents.sql_agent import create_sql_agent
from langgraph.checkpoint.sqlite import SqliteSaver

def create_analyst_bot(db):
    sql_tools = create_sql_tools(
        db=db,
        llm=llm
    )
    sql_generation_tools = [
        sql_tools["sql_db_list_tables"],
        sql_tools["sql_db_schema"],
        sql_tools["sql_db_query_checker"]
    ]

    execution_tool = sql_tools["sql_db_query"]
    sql_agent = create_sql_agent(sql_generation_tools)
    generate_sql = create_generate_sql_node(sql_agent)
    insight_node = create_execute_and_generate_insights_node(execution_tool)

    graph = StateGraph(SQLAgentState)

    graph.add_node("sql_generator", generate_sql)
    graph.add_node("sql_reviewer", review_sql)
    graph.add_node("execute_and_insight", insight_node)
    graph.add_node("visualisation_node", visualisation_node)

    graph.add_edge(START, "sql_generator")
    graph.add_edge("sql_generator", "sql_reviewer")
    graph.add_conditional_edges(
        "sql_reviewer",
        route_after_review,
        {
            "sql_generator": "sql_generator",
            "execute_and_insight": "execute_and_insight",
        }
    )
    #graph.add_edge("execute_and_insight", "visualisation_node")
    #graph.add_edge("visualisation_node", END)
    
    memory = SqliteSaver.from_conn_string(
    "checkpoints.db"
)

    return graph.compile(checkpointer=memory)