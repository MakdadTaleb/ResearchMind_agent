from langchain_core.messages import HumanMessage
from api.dependencies import get_graph
from api.schemas.research import ResearchResponse
from utils.input_validator import validate_input
from utils.langfuse_logger import flush
from fastapi import HTTPException
from utils.langfuse_logger import observe, flush
import uuid
from repositories.reports_repository import save_report


async def validate_data(topic: str)-> None:
    is_valid, reason = await validate_input(topic)
    if not is_valid:
        raise HTTPException(status_code=400, detail=reason)
    
def init_state(topic: str)-> dict:
    initial_state = {
        "topic": topic,
        "messages": [HumanMessage(content=f"Research topic: {topic}")],
        "search_results": "",
        "summaries": "",
        "analysis": "",
        "final_report": "",
        "next": ""
    }
    
    return initial_state


@observe(name="research_pipeline")
async def run_research(topic: str, user_id: str) -> ResearchResponse:

    # --- Validate input ---
    await validate_data(topic)

    initial_state = init_state(topic)

    graph = await get_graph()

    try:
        result = await graph.ainvoke(
            initial_state,
            config={
                    "recursion_limit": 20,
                    "configurable": {"thread_id": str(uuid.uuid4())}
                }
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Research failed: {str(e)}")
    
    if result.get("error"):
        raise HTTPException(status_code=500, detail=f"Pipeline failed: {result['error']}")

    if not result.get("final_report"):
        raise HTTPException(status_code=500, detail="No report generated.")
    
    # --- Save report to database ---
    await save_report(
        user_id=user_id,
        topic=topic,
        final_report=result["final_report"]
    )
    
    # --- Flush logs to Langfuse ---
    flush()

    return ResearchResponse(
        topic=topic,
        final_report=result.get("final_report", ""),
        status="success"
    )


async def _stream_graph_events(graph, initial_state: dict, full_report: dict):
    yield "data: 🔍 Starting research...\n\n"

    async for event in graph.astream_events(
        initial_state,
        config={
            "recursion_limit": 20,
            "configurable": {"thread_id": str(uuid.uuid4())}
        },
        version="v2"
    ):
        if (
            event["event"] == "on_chat_model_stream" and
            event.get("metadata", {}).get("langgraph_node") == "writer_agent"
        ):
            chunk = event["data"]["chunk"].content
            if chunk:
                full_report["text"] += chunk
                yield f"data: {chunk}\n\n"

        elif event["event"] == "on_chain_start":
            node = event.get("metadata", {}).get("langgraph_node", "")
            if node == "search_agent":
                yield "data: \n\n🔍 Searching for papers...\n\n"
            elif node == "reader_agent":
                yield "data: \n\n📖 Reading papers...\n\n"
            elif node == "analyzer_agent":
                yield "data: \n\n🔬 Analyzing papers...\n\n"
            elif node == "writer_agent":
                yield "data: \n\n✍️ Writing Literature Review...\n\n"

    yield "data: [DONE]\n\n"
    flush()


@observe(name="research_pipeline_stream")
async def run_research_stream(topic: str, user_id: str):
    await validate_data(topic)
    initial_state = init_state(topic)
    graph = await get_graph()
    full_report = {"text": ""}
    async def generate():
        try:
            async for chunk in _stream_graph_events(graph, initial_state, full_report):
                yield chunk

            # --- Save report to database ---
            await save_report(
                user_id=user_id,
                topic=topic,
                final_report=full_report["text"]
            )
        except Exception as e:
            yield f"data: ❌ Error: {str(e)}\n\n"
    
    

    return generate()
