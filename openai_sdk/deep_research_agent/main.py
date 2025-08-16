import asyncio
from agents import Runner, trace, gen_trace_id
from search import search_agent
from planner import WebSearchItem, WebSearchPlan, planner_agent
from writer import ReportData, writer_agent
from email_agent import email_agent


class ResearchManager:
    async def run(self, query: str):
        """Run the deep research process, yielding status updates and the final output"""
        trace_id = gen_trace_id()
        with trace("Research trace", trace_id=trace_id):
            url = f"https://platform.openai.com/traces/trace?trace_id={trace_id}"
            print(f"View trace: {url}")
            yield f"View trace: {url}"

            print("Starting research...")
            plan_search = await self.plan_searches(query)
            yield "Searches planned, starting search phase..."

            search_results = await self.perform_searches(plan_search)
            yield "Searching complete, writing report..."

            report = await self.write_report(query, search_results)
            yield "Report written, sending email..."

            await self.send_email(report)
            yield "Email sent, research complete ✅"
            yield report.markdown_report

    async def plan_searches(self, query: str) -> WebSearchPlan:
        """Plan searches from the planner agent"""
        print("Planning searches...")
        result = await Runner.run(planner_agent, f"Query: {query}")
        plan = result.final_output_as(WebSearchPlan)
        print(f"Will perform {len(plan.searches)} searches")
        return plan

    async def perform_searches(self, search_plan: WebSearchPlan) -> list[str]:
        """Perform all searches concurrently"""
        print("Performing searches...")
        results = []
        tasks = [asyncio.create_task(self.search(item)) for item in search_plan.searches]

        num_completed = 0
        for task in asyncio.as_completed(tasks):
            r = await task
            if r is not None:
                results.append(r)
            num_completed += 1
            print(f"Searching... {num_completed}/{len(tasks)} completed")

        print("Finished all searches.")
        return results

    async def search(self, item: WebSearchItem) -> str | None:
        """Perform the search for a given query item"""
        print(f"Searching for: {item.query}")
        input_text = f"Original Query: {item.query}\nReason for searching: {item.reason}"
        try:
            result = await Runner.run(search_agent, input_text)
            return str(result.final_output)
        except Exception as e:
            print(f"Search failed: {e}")
            return None

    async def write_report(self, query: str, search_results: list[str]) -> ReportData:
        """Write the final research report"""
        print("Writing report...")
        input_text = f"Original Query: {query}\nSummarized search results: {search_results}"
        result = await Runner.run(writer_agent, input_text)
        print("Finished writing report.")
        return result.final_output_as(ReportData)

    async def send_email(self, report: ReportData):
        """Send the final report via email"""
        print("Sending email...")
        await Runner.run(email_agent, report.markdown_report)
        print("Email sent.")
        return report








        