from langchain.agents import create_agent
from config.llm import llm
from prompts.visualisation_prompt import VISUALISATION_PROMPT
from states.chart import VisualisationOutput

visualisation_agent = create_agent(
    model=llm,
    system_prompt=VISUALISATION_PROMPT,
    response_format=VisualisationOutput
)
