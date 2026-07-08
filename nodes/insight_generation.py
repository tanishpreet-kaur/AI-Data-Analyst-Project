from states.analyst_state import AnalystState
from config.llm import llm
from pydantic import BaseModel
from prompts.insight_prompt import INSIGHT_PROMPT

class InsightReport(BaseModel):
    answer: str

def insight_generation_node(state: AnalystState):
    try: 
        insight_agent = llm.with_structured_output(InsightReport)
        response = insight_agent.invoke(
            [
                (
                    "system",
                    INSIGHT_PROMPT,
                ),
                (
                    "human",
                    f"""
                        User Question: {state["question"]}
                        SQL Query: {state["sql_query"]}
                        Query Result: {state["query_result"]}
                        """
                ),
            ]
        )

        return {
            "answer": response.answer,
            "error": None,
        }

    except Exception as e:
        print(e)
        raise