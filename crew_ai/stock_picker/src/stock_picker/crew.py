import yaml
from pathlib import Path
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool
from pydantic import BaseModel, Field
from typing import List
from crewai.memory import LongTermMemory, ShortTermMemory, EntityMemory
from crewai.memory.storage.rag_storage import RAGStorage
from crewai.memory.storage.ltm_sqlite_storage import LTMSQLiteStorage
from stock_picker.tools.push_tool import PushNotificationTool



class TrendingCompany(BaseModel):
    name: str = Field(description="The name of the company")
    ticker: str = Field(description="Stock ticker symbol")
    reason: str = Field(description="Reason this company is trending in the news")


class TrendingCompanyList(BaseModel):
    companies: List[TrendingCompany] = Field(description="List of trending companies")


class TrendingCompanyResearch(BaseModel):
    name: str = Field(description="The name of the company")
    market_position: str = Field(description="The market position of the company")
    future_outlook: str = Field(description="Future outlook and growth prospects")
    investment_potential: str = Field(description="Investment potential and suitability of investment")


class TrendingCompanyResearchList(BaseModel):
    research_list: List[TrendingCompanyResearch] = Field(
        description="Comprehensive research on all listed companies"
    )


@CrewBase
class StockPicker:
    """Stock picker crew that finds, researches, and selects trending companies"""

    
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def trending_company_finder(self) -> Agent:
        return Agent(
            config=self.agents_config["trending_company_finder"],
            tools=[SerperDevTool()],
            memory=True
        )

    @agent
    def financial_researcher(self) -> Agent:
        return Agent(
            config=self.agents_config["financial_researcher"],
            tools=[SerperDevTool()],
            memory=True
        )

    @agent
    def stock_picker(self) -> Agent:
        return Agent(
            config=self.agents_config["stock_picker"],
            tools=[PushNotificationTool()],
            memory=True
        )

    @task
    def find_trending_company(self) -> Task:
        return Task(
            config=self.tasks_config["find_trending_company"],
            output_pydantic=TrendingCompanyList
        )

    @task
    def research_trending_companies(self) -> Task:
        return Task(
            config=self.tasks_config["research_trending_companies"],
            output_pydantic=TrendingCompanyResearchList
        )

    @task
    def pick_best_company(self) -> Task:
        return Task(
            config=self.tasks_config["pick_best_company"]
        )

    @crew
    def crew(self) -> Crew:
        manager = Agent(
            config=self.agents_config["manager"],
            allow_delegation=True
        )

        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.hierarchical,
            verbose=True,
            manager_agent=manager,
            memory=True,
            long_term_memory=LongTermMemory(
                storage=LTMSQLiteStorage(
                    db_path="./memory/long_term_memory_storage.db"
                )
            ),
            short_term_memory=ShortTermMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {"model": 'text-embedding-3-small'}
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
            entity_memory=EntityMemory(
                storage=RAGStorage(
                    embedder_config={
                        "provider": "openai",
                        "config": {"model": 'text-embedding-3-small'}
                    },
                    type="short_term",
                    path="./memory/"
                )
            ),
        )







