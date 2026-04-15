from agents.prompts.search_prompt import get_search_prompt
from agents.llm import llm
from agents.state import ResearchState
from tools.search_tool_tavily import search_research_papers
from langchain_core.messages import SystemMessage, AIMessage, HumanMessage
from utils.langfuse_logger import observe


@observe(name="search_agent")
async def search_agent_node(state: ResearchState):

    prompt = get_search_prompt(
        topic=state["topic"]
    )
    
    llm_with_tools = llm.bind_tools([search_research_papers])
    messages = [SystemMessage(content=prompt)]
    all_results = []

    print("\n🔍 Search Agent: Searching for papers...")

    for i in range(3):
        try:
            response = await llm_with_tools.ainvoke(messages)
            messages.append(response)

            if not hasattr(response, "tool_calls") or not response.tool_calls:
                messages.append(HumanMessage(
                    content=f"You must do search number {i+1}. Call the search tool now."
                ))
                response = await llm_with_tools.ainvoke(messages)
                messages.append(response)

            if hasattr(response, "tool_calls") and response.tool_calls:
                for tool_call in response.tool_calls:
                    try:
                        result = await search_research_papers.ainvoke(tool_call["args"])
                        if result:
                            all_results.append(result)
                    except Exception as e:
                        print(f"   ⚠️ Tool call failed: {str(e)}")
                        continue
                print(f"   ✅ Search {i+1} completed")

        except Exception as e:
            print(f"   ⚠️ Search {i+1} failed: {str(e)}")
            import asyncio
            await asyncio.sleep(2) 
            continue

    if not all_results:
        print("   ❌ All searches failed")
        return {
            "search_results": "",
            "error": "search_failed",
            "messages": [AIMessage(content="Search failed. No results found.")]
        }

    combined_results = "\n\n---\n\n".join(all_results)
    combined_results = combined_results[:8000]

    print(f"\n🔎 Search result sample:\n{combined_results[:400]}")

    return {
        "search_results": combined_results,
        "messages": [AIMessage(content=f"Search completed:\n{combined_results[:300]}...")]
    }