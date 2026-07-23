from states.analyst_state import AnalystState
from config.llm import llm
from prompts.insight_prompt import INSIGHT_PROMPT

def insight_generation_node(state: AnalystState):
    try: 
        response = llm.invoke(
                        [
                            ("system", INSIGHT_PROMPT),
                            (
                                "human",
                                f"""
                                User Question: {state['question']}
                                SQL Query: {state['sql_query']}
                                Query Result: {state['query_result']}
                                """
                            ),
                        ]
                    )
        return {
            "answer": response.content,
            "error": None,
        }

    except Exception as e:
        print(e)
        raise