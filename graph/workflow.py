from langgraph.graph import StateGraph, START, END
from states.analyst_state import AnalystState
from nodes.sql_generation import sql_generation_node
from nodes.sql_execution import sql_execution_node

graph = StateGraph(AnalystState)

graph.add_node("sql_generator", sql_generation_node)
graph.add_node("sql_executor", sql_execution_node)

graph.add_edge(START, "sql_generator")
graph.add_edge("sql_generator", "sql_executor")

analyst_bot = graph.compile()
