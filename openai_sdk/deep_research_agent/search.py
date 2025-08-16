from agents import Agent, WebSearchTool, ModelSettings

INSTRUCTIONS = (
    "You are a search assistant. Given a search term, you search the web for that term "
    "and produce a concise summary of the results. The summary should be 2–3 paragraphs, "
    "under 300 words, and capture the main points clearly. The output will be consumed "
    "by someone synthesizing a report, so it is vital to capture the essence accurately."
)

search_agent = Agent(
    name="search_agent",
    instructions=INSTRUCTIONS,
    tools=[WebSearchTool(search_context_size="low")],
    model="gpt-4o-mini",
    model_settings=ModelSettings(tool_choice="required"),
)
