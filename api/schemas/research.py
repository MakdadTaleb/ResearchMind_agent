from pydantic import BaseModel, Field

class ResearchRequest(BaseModel):
    topic: str = Field(..., example="The impact of climate change on marine biodiversity")

class ResearchResponse(BaseModel):
    topic: str
    final_report: str
    status: str


