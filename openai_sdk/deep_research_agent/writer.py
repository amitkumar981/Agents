from pydantic import BaseModel, Field
from agents import Agent

INSTRUCTIONS = (
    "You are a senior researcher tasked with writing a cohesive report for a research query. "
    "You will be provided with an original query and some initial research from assistants. "
    "First, create an outline for the report and describe the structure you will follow. "
    "Then, generate the full report. "
    "The final report must be in Markdown format, detailed, and comprehensive."
)

class ReportData(BaseModel):
    short_summary: str = Field(
        description="A concise 2–3 sentence summary of the findings"
    )
    markdown_report: str = Field(
        description="The full detailed report in Markdown format"
    )
    follow_up_questions: list[str] = Field(
        description="Suggested topics or questions for further research"
    )

writer_agent = Agent(
    name="writer_agent",
    instructions=INSTRUCTIONS,
    model="gpt-4o-mini",
    output_type=ReportData,
)
