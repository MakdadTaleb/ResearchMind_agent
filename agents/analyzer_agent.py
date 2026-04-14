from langchain_core.messages import AIMessage, SystemMessage
from agents.prompts.analyzer_prompt import get_analyzer_prompt
from agents.llm import llm
from agents.state import ResearchState
from utils.langfuse_logger import observe


# --- Analyzer Agent Node ---
@observe(name="analyzer_agent")
async def analyzer_agent_node(state: ResearchState):

   print("\n🔬 Analyzer Agent: Analyzing and comparing papers...")

   prompt = get_analyzer_prompt(
        summaries=state.get("summaries", "No summaries found"),
        topic=state["topic"]
    )
    
   print("\n🔬 Analyzer Agent: Analyzing and comparing papers...")

   messages = [SystemMessage(content=prompt)]
   response = await llm.ainvoke(messages)

   if not response.content:
      return {
         "analysis": "",
         "error": "analyzer_failed", 
         "messages": [AIMessage(content="Analysis failed.")]
      }
   
   print("   ✅ Analysis completed")
   
   return {
         "analysis": response.content,
         "messages": [AIMessage(content=f"Analysis completed:\n{response.content[:500]}...")]
      }