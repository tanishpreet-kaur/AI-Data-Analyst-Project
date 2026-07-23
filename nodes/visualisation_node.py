from states.analyst_state import AnalystState
from agents.visualisation_agent import visualisation_agent

def visualisation_node(state: AnalystState):
    df = state["query_result"]

    response = visualisation_agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                            Question:
                            {state["question"]}

                            Columns:
                            {list(df.columns)}

                            SQL Result:
                            {df.to_json(orient="records")}
                            """
                }
            ]
        }
    )

    return {
        "chart_spec": response["structured_response"]
    }