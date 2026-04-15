from agents.prompts.reader_prompt import get_reader_prompt
from agents.llm import llm
from agents.state import ResearchState
from langchain_core.messages import SystemMessage, AIMessage
from utils.langfuse_logger import observe

@observe(name="reader_agent")
async def reader_agent_node(state: ResearchState):
    
    print("\n📖 Reader Agent: Reading and summarizing papers...")

    prompt = get_reader_prompt(
        search_results=state.get("search_results", "No results found"),
        topic=state["topic"]
    )

    messages = [SystemMessage(content=prompt)]
    response = await llm.ainvoke(messages)

    if not response.content:
        return {
            "summaries": "",
            "error": "reader_failed",
            "messages": [AIMessage(content="Reading failed.")]
        }
    print("   ✅ Summarization completed")

    return {
        "summaries": response.content,
        "messages": [AIMessage(content=f"Reading completed. Summarized papers:\n{response.content[:500]}...")]
    }