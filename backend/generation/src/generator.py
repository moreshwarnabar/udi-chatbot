from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase,agent, task, crew, before_kickoff

@CrewBase
class GeneratorCrew():

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    def __init__(self, model:str = 'groq/llama-3.3-70b-versatile'):
        self.model = model

    @agent
    def generator(self) -> Agent:
        return Agent(
            config=self.agents_config['generator'],
            llm=LLM(model=self.model),
            verbose=False
        )
    
    @agent
    def formatter(self) -> Agent:
        return Agent(
            config=self.agents_config['formatter'],
            llm=LLM(model=self.model),
            verbose=False
        )
    
    @task
    def generator_task(self) -> Task:
        return Task(
            config=self.tasks_config['generation_task']
        )
    
    @task
    def formatting_task(self) -> Task:
        return Task(
            config=self.tasks_config['formatting_task']
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=False
        )