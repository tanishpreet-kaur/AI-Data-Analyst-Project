from states.analyst_state import AnalystState
from states.chart import ChartSpec
from prompts.visualisation_prompt import VISUALIZATION_PROMPT
from config.llm import llm

def visualisation_node(state: AnalystState):
    try:
        visualization_agent = llm.with_structured_output(ChartSpec)
        chart = visualization_agent.invoke(
            [
                (
                    "system",
                    VISUALIZATION_PROMPT,
                ),
                (
                    "human",
                    f"""
                        Question: {state["question"]}
                        SQL: {state["sql_query"]}
                        Result: {state["query_result"]}
                        """
                )
            ]
        )

        return {
            "chart_spec": chart
        }

    except Exception as e:

        return {
            "chart_spec": None,
            "error": str(e)
        }