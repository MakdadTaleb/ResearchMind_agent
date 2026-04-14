from agents.supervisor import ResearchState, supervisor_node
from agents.search_agent import search_agent_node
from agents.reader_agent import reader_agent_node
from agents.analyzer_agent import analyzer_agent_node
from agents.writer_agent import writer_agent_node
from typing import Literal
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
import os
from dotenv import load_dotenv

load_dotenv()

db_url = (
    f"postgresql://postgres:{os.getenv('DB_PASSWORD')}"
    f"@db.{os.getenv('DB_HOST')}.supabase.co:5432/postgres"
)

# ---- Router : supervisor decides who works next ----
def route(state: ResearchState) -> Literal[
    "search_agent", 
    "reader_agent", 
    "analyzer_agent", 
    "writer_agent", 
    "__end__"
    ]:

    next_agent = state.get("next" , "search_agent")

    if next_agent == "FINISH":
        return END
    
    return next_agent

# ---- build graph ----
async def build_graph():
    
    # db_url = os.getenv("DATABASE_URL")
    
    # async with AsyncPostgresSaver.from_conn_string(db_url) as checkpointer:
    #     await checkpointer.setup()
    
    checkpointer = MemorySaver()

    graph = StateGraph(ResearchState)

    graph.add_node("supervisor", supervisor_node)
    graph.add_node("search_agent", search_agent_node)
    graph.add_node("reader_agent", reader_agent_node)
    graph.add_node("analyzer_agent", analyzer_agent_node)
    graph.add_node("writer_agent", writer_agent_node)

    graph.set_entry_point("supervisor")
    graph.add_conditional_edges("supervisor", route)

    graph.add_edge("search_agent", "supervisor")
    graph.add_edge("reader_agent", "supervisor")
    graph.add_edge("analyzer_agent", "supervisor")
    graph.add_edge("writer_agent", "supervisor")

    return graph.compile(checkpointer=checkpointer)


