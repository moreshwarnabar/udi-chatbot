from crewai import Agent, Task, Crew
from crewai.project import agent, task, crew

class GeneratorCrew():
    @agent
    def generator(self) -> Agent:
        return Agent(
            config=self.agents_config['generator'],
            verbose=True
        )
    
    @task
    def generator_task(self) -> Task:
        return Task(
            config=self.tasks_config['generation_task']
        )
    
    @crew
    def generator_crew(self) -> Crew:
        return Crew(
            agent=self.agents,
            task=self.tasks,
            verbose=True
        )