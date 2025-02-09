#!/usr/bin/env python
import sys
import os
from textwrap import dedent
from agent_bravo.crew import AgentBravoCrew
from agent_bravo.models.gov_decision import GovDecision
from agent_bravo.utils import get_proposal_created_events, get_proposal_status, publish_opinion_and_vote, has_voted

POLICY = dedent("""
    Vote NO Conditions
    The proposal does not clearly demonstrate a return on investment (ROI) of at least 10% annually.

    Vote YES Conditions
    The proposal clearly demonstrates a return on investment (ROI) of at least 10% annually.

    Vote ABSTAIN Conditions
    The proposal's return on investment (ROI) cannot be accurately determined from the provided information.
""")

BACKSTORY = dedent("""
    I am a seasoned delegate with experience reviewing governance proposals.
""")

def run():
    """
    Run Agent Bravo with a proposal and policy as inputs.
    """
    # --- Get Proposals ---
    proposals = get_proposal_created_events()
    print(f"Found {len(proposals)} proposals all time.")

    # --- Process Proposals ---
    for proposal in proposals:
        print(f"\n=== Processing Proposal ===")
        print(f"Proposal ID: {proposal['proposalId']}")
        print(f"Description: {proposal['description']}")
        print("===========================\n")
        proposal_id = proposal['proposalId']
        description = proposal['description']

        # --- Check Proposal Status is Active ---
        status = get_proposal_status(proposal_id)
        print(f"Proposal Status: {status}")

        if status != 'active':
            print(f"Proposal {proposal_id} is not active, skipping...")
            continue

        # --- Check if the delegate has already voted ---
        if has_voted(proposal_id, os.getenv('DELEGATE_ADDRESS')):
            print(f"Delegate has already voted on proposal {proposal_id}, skipping...")
            continue

        # --- Setup Agent Bravo Crew to handle the active proposal ---
        agent_bravo = AgentBravoCrew()
        crew = agent_bravo.crew()
        inputs = {
            'proposal': description,
            'policy': POLICY,
            'backstory': BACKSTORY
        }
        crew.kickoff(inputs=inputs)

        # --- Review the proposal and make a decision ---
        # Convert results (GovDecision) to dictionary format.
        # {
        #     'opinion': 'The opinion of the agent',
        #     'reasoning': 'The reasoning behind the opinion',
        #     'vote': 0, 1, or 2 (0 = against, 1 = for, 2 = abstain)
        # }
        gov_decision_dict = agent_bravo.review_task().output.to_dict()
        gov_decision = GovDecision(**gov_decision_dict)

        # # --- Publish the decision to the blockchain ---
        # tx_receipt = publish_opinion_and_vote(gov_decision)

        # --- Print Decision Summary ---
        print("\n=== Governance Decision Summary ===")
        print(f"Opinion: \n{gov_decision.opinion}\n")
        print(f"Reasoning: \n{gov_decision.reasoning}\n")
        print(f"Vote: {'AGAINST' if gov_decision.vote == 0 else 'FOR' if gov_decision.vote == 1 else 'ABSTAIN'}")
        # print(f"Transaction Hash: {tx_receipt['transactionHash'].hex() if tx_receipt else 'N/A'}")
        print("================================\n")
        
    return 0

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
