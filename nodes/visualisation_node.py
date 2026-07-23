from states.analyst_state import AnalystState
from states.chart import ChartSpec
from prompts.visualisation_prompt import VISUALISATION_PROMPT
from config.llm import llm
from agents.visualisation_agent import visualisation_agent

def visualisation_node(state: AnalystState):
    try:
        response = visualisation_agent.invoke(
            {
                "messages": [
                    {
                        "role": "user",
                        "content": f"""
                            Question:

                            {state['question']}

                            SQL Result:

                            {state['query_result'].to_json(orient='records')}
                            """
                    }
                ]
            }
        )

        state["chart_spec"] = response["structured_response"]


    except Exception as e:
        return {
            "chart_spec": None,
            "error": str(e)
        }