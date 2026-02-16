import os
from langchain_anthropic import ChatAnthropic

# LangChain will automatically look for ANTHROPIC_API_KEY in your Render Env
llm = ChatAnthropic(
    model="claude-3-5-sonnet-latest",
    temperature=0.2
)
