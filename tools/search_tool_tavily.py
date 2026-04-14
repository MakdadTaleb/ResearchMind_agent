from langchain_core.tools import tool
from tavily import TavilyClient
import os
from dotenv import load_dotenv

load_dotenv()

tavily = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))

@tool
def search_research_papers(query: str) -> str:
    """
    Search for real academic papers and research on a given topic.
    Use this tool to find recent publications, studies, and research findings.
    
    Input: A specific research topic or question
    Output: List of papers with titles, summaries, and source URLs
    """
    try:
        response = tavily.search(
            query=f"research paper academic {query}",
            search_depth="advanced",
            max_results=3,
            include_answer=True,
        )

        result = ""

        if response.get("answer"):
            result += f"Overview: {response['answer'][:800]}\n\n"

        for i, item in enumerate(response.get("results", []), 1):
            result += f"{i}. {item.get('title', 'No title')}\n"
            result += f"   Summary: {item.get('content', '')[:800]}\n"
            result += f"   URL: {item.get('url', '')}\n\n"

        return result[:5000]  
    except Exception as e:
        return f"Error: {str(e)}"