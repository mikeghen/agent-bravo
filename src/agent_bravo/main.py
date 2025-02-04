#!/usr/bin/env python
import sys
from textwrap import dedent
from agent_bravo.crew import AgentBravoCrew
from agent_bravo.models.gov_decision import GovDecision

# TODO: Get proposal and policy from DAO by reading the latest event on the blockchain.
PROPOSAL = "Spend $1.5 million to pay people to use the DAO's product."
POLICY = dedent("""
    Proposals requesting funds from the treasury must show how the funds will be used to generate a return on investment (ROI) for the DAO.
    Proposals that show a return on investment (ROI) of GREATER THAN 10% in a year will be voted for.
    Proposals that show a return on investment (ROI) of LESS THAN 10% in a year will be voted against.
    Proposals that do not show how the funds will be used to generate a return on investment (ROI) will be voted against.
""")

def run():
    """
    Run Agent Bravo with a proposal and policy as inputs.
    """
    agent_bravo = AgentBravoCrew()
    crew = agent_bravo.crew()
    inputs = {
        'proposal': PROPOSAL,
        'policy': POLICY,
    }
    crew.kickoff(inputs=inputs)

    # Convert results (GovDecision) to dictionary format.
    # {
    #     'opinion': 'The opinion of the agent',
    #     'reasoning': 'The reasoning behind the opinion',
    #     'vote': 0, 1, or -1
    # }
    gov_decision_dict = agent_bravo.review_task().output.to_dict()
    print(f"GovDecision: {gov_decision_dict}")
    print(f"Opinion: {gov_decision_dict['opinion']}")
    print(f"Reasoning: {gov_decision_dict['reasoning']}")
    print(f"Vote: {gov_decision_dict['vote']}")

    gov_decision = GovDecision(**gov_decision_dict)
    print(f"GovDecision: {gov_decision}")
    print(f"Opinion: {gov_decision.opinion}")
    print(f"Reasoning: {gov_decision.reasoning}")
    print(f"Vote: {gov_decision.vote}")




def train():
    """
    Train the crew for a given number of iterations.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AgentBravoCrew().crew().train(n_iterations=int(sys.argv[1]), filename=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while training the crew: {e}")

def replay():
    """
    Replay the crew execution from a specific task.
    """
    try:
        AgentBravoCrew().crew().replay(task_id=sys.argv[1])

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")

def test():
    """
    Test the crew execution and returns the results.
    """
    inputs = {
        "topic": "AI LLMs"
    }
    try:
        AgentBravoCrew().crew().test(n_iterations=int(sys.argv[1]), openai_model_name=sys.argv[2], inputs=inputs)

    except Exception as e:
        raise Exception(f"An error occurred while replaying the crew: {e}")
