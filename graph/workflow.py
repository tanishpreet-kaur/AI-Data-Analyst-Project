from langgraph.graph import StateGraph, START, END
from states.analyst_state import AnalystState
from nodes.sql_generation import sql_generation_node
from nodes.sql_execution import sql_execution_node
from nodes.insight_generation import insight_generation_node
from nodes.visualisation_node import visualisation_node

graph = StateGraph(AnalystState)

graph.add_node("sql_generator", sql_generation_node)
graph.add_node("sql_executor", sql_execution_node)
graph.add_node("insight_generator", insight_generation_node)
graph.add_node("visualisation_generator", visualisation_node)

graph.add_edge(START, "sql_generator")
graph.add_edge("sql_generator", "sql_executor")
graph.add_edge("sql_executor", "insight_generator")
graph.add_edge("insight_generator", "visualisation_generator")
graph.add_edge("visualisation_generator", END)

analyst_bot = graph.compile()
