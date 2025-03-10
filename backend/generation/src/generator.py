from crewai import Agent, Task, Crew, LLM
from crewai.project import CrewBase,agent, task, crew, before_kickoff

@CrewBase
class GeneratorCrew():

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @agent
    def generator(self, model:str = 'groq/llama-3.3-70b-versatile') -> Agent:
        return Agent(
            config=self.agents_config['generator'],
            llm=LLM(model=model),
            verbose=True
        )
    
    @task
    def generator_task(self) -> Task:
        return Task(
            config=self.tasks_config['generation_task']
        )
    
    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            verbose=True
        )