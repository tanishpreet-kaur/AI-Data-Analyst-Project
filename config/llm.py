from config.settings import OPENROUTER_API_KEY
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    model_name="nvidia/nemotron-3-ultra-550b-a55b:free"
)