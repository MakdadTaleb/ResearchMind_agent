from langchain_core.messages import HumanMessage
from graph import app
from utils.input_validator import validate_input
from utils.langfuse_logger import observe, flush

@observe(name="research_pipeline")
def run_research(topic: str):
    print(f"\n🔬 Starting research on: {topic}")
    print("=" * 50)

    is_valid, reason = validate_input(topic)
    if not is_valid:
        print(f"\n🚫 Input rejected: {reason}")
        return None

    initial_state = {
        "topic": topic,
        "messages": [HumanMessage(content=f"Research topic: {topic}")],
        "search_results": "",
        "summaries": "",
        "analysis": "",
        "final_report": "",
        "next": ""
    }

    
    try:
        result = app.invoke(
            initial_state,
            config={"recursion_limit": 20}
        )
    except Exception as e:
        print(f"\n❌ Research failed: {str(e)}")
        return None

    if not result.get("final_report"):
        print("\n❌ No report generated.")
        return None

    print("\n📋 FINAL LITERATURE REVIEW:")
    print("=" * 50)
    print(result["final_report"])

    try:
        with open(f"report_{topic[:30].replace(' ', '_')}.md", "w", encoding="utf-8") as f:
            f.write(result["final_report"])
        print(f"\n✅ Report saved!")
    except Exception as e:
        print(f"\n⚠️ Could not save report: {str(e)}")

    flush()
    return result


if __name__ == "__main__":
    topic = input("Enter research topic: ")
    run_research(topic)