from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

load_dotenv()


# ---- shared LLM for all agents ----
llm = ChatGroq(
    model=os.getenv("GROQ_MODEL"), 
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.1
)