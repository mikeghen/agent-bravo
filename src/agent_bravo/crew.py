from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from agent_bravo.models.gov_decision import GovDecision

# Uncomment the following line to use an example of a custom tool
# from agent_bravo.tools.custom_tool import MyCustomTool

# Check our tools documentations for more information on how to use them
# from crewai_tools import SerperDevTool

@CrewBase
class AgentBravoCrew():
	"""AgentBravo crew"""

	@agent
	def delegate(self) -> Agent:
		return Agent(
			config=self.agents_config['delegate'],
			verbose=True
		)

	@task
	def review_task(self) -> Task:
		"""Creates a task for the review agent with a structured output"""
		return Task(
			config=self.tasks_config['review_task'],
			output_json=GovDecision
		)

	@crew
	def crew(self) -> Crew:
		"""Creates the AgentBravo crew"""
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True,
		)