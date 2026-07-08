from agents.sql_agent import create_sql_agent

def sql_generation_node(state):
    agent = create_sql_agent(state["database"])
    response = agent.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": f"""
                        Question:
                        {state['question']}

                        Schema:
                        {state['database_context'].schema}

                        Generate ONLY SQL.
                        """
                }
            ]
        }
    )

    return {
        "sql_query": response["messages"][-1].content
    }