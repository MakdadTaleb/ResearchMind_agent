# ---- Shared state for all agents ---- 
import operator
from typing import Annotated, TypedDict


class ResearchState(TypedDict):
    topic: str                                    # research project
    #----------------------------question to claude-----------------------------
    messages: Annotated[list, operator.add]       # all messages
    search_results: str                           # results of the search
    summaries: str                                # summaries of the research
    analysis: str                                 # analysis and compare
    final_report: str                             # final report
    next: str                                     # Any Agent works next ?
    error: str                                    # Any error happens ?
    