from agents.sql_agent import create_sql_agent

DESTRUCTIVE_SENTINEL = "DESTRUCTIVE_REQUEST"

def sql_generation_node(state):
    agent = create_sql_agent(state["database"])
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                        Question: {state['question']}
                        Schema: {state['database_context'].schema}
                        Generate ONLY SQL.
                        """
                }
            ]
        }
    )

    content = response["messages"][-1].content.strip()

    if content == DESTRUCTIVE_SENTINEL:
        return {
            "sql_query": None,
            "review_status": "BLOCKED",
            "answer": "cannot execute this",
        }

    return {"sql_query": content}