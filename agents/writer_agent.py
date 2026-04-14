from langchain_core.messages import AIMessage, SystemMessage
from agents.prompts.writer_prompt import get_writer_prompt
from agents.llm import llm
from agents.state import ResearchState
from utils.langfuse_logger import observe

# --- Writer Agent Node ---
@observe(name="writer_agent")

async def writer_agent_node(state: ResearchState):
       
    print("\n✍️  Writer Agent: Writing Literature Review...")

    prompt= get_writer_prompt(
        topic=state["topic"],
        summaries=state.get("summaries", ""),
        analysis=state.get("analysis", "")
    )


    messages = [SystemMessage(content=prompt)]
    response = await llm.ainvoke(messages)

    if not response.content:
        return {
            "final_report": "",
            "error": "writer_failed",
            "messages": [AIMessage(content="Writing failed.")]
        }

    print("   ✅ Literature Review completed")

    return {
        "final_report": response.content,
        "messages": [AIMessage(content="Literature Review written successfully! ✅")]
    }