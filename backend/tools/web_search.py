from tavily import TavilyClient
import os

client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

def web_search(query: str):
    return client.search(
        query=query,
        search_depth="advanced",
        include_sources=True,
        max_results=8
    )
