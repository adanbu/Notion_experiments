from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from tools.notion_search_tool2 import NotionSearchTool

from dotenv import load_dotenv
load_dotenv()


@CrewBase
class TestingCrew:

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def search_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['search_agent'],
            tools=[NotionSearchTool()],
            verbose =True,
            allow_delegation=False
        )
    
    @task
    def search_task(self) -> Task:
        return Task(
            config = self.tasks_config['search_task'],
            agent=self.search_agent()
            )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks, 
            process=Process.sequential,
            verbose=True
        )