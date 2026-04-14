from agents.state import ResearchState


def supervisor_node(state: ResearchState):

    if state.get("error"):
        print(f"\n🎯 Supervisor: Error detected → FINISH")
        return {"next": "FINISH"}

    if not state.get("search_results"):
        print("\n🎯 Supervisor decision: → search_agent")
        return {"next": "search_agent"}

    if not state.get("summaries"):
        print("\n🎯 Supervisor decision: → reader_agent")
        return {"next": "reader_agent"}

    if not state.get("analysis"):
        print("\n🎯 Supervisor decision: → analyzer_agent")
        return {"next": "analyzer_agent"}

    if not state.get("final_report"):
        print("\n🎯 Supervisor decision: → writer_agent")
        return {"next": "writer_agent"}

    print("\n🎯 Supervisor decision: → FINISH")
    return {"next": "FINISH"}







