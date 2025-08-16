from pydantic import BaseModel, Field
from agents import Agent

# Number of searches to generate
HOW_MANY_SEARCHES = 2

INSTRUCTIONS = (
    f"You are a helpful research assistant. For the given query, "
    f"come up with a set of web searches to perform in order to provide the best answer. "
    f"Output {HOW_MANY_SEARCHES} search terms."
)

class WebSearchItem(BaseModel):
    reason: str = Field(description="Explain why this search is important for answering the query")
    query: str = Field(description="The search term to use for the web search")

class WebSearchPlan(BaseModel):
    searches: list[WebSearchItem] = Field(
        description="The list of web searches to perform to find the best answer"
    )

planner_agent = Agent(
    name="planner_agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=WebSearchPlan,
)
