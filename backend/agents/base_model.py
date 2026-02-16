import os
from langchain_anthropic import ChatAnthropic

# Using 3.5 Sonnet: Best balance of speed, cost, and complex reasoning
llm = ChatAnthropic(
    model="claude-3-5-sonnet-20240620",
    temperature=0,  # Zero for factual accuracy
    anthropic_api_key=os.getenv("ANTHROPIC_API_KEY")
)
