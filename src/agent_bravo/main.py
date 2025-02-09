#!/usr/bin/env python
import sys
import os
from textwrap import dedent
from agent_bravo.crew import AgentBravoCrew
from agent_bravo.models.gov_decision import GovDecision
from agent_bravo.utils import get_proposal_created_events, get_proposal_status, publish_opinion_and_vote, get_voting_policy


def run():
    """
    Run Agent Bravo with a proposal and policy as inputs.
    """
    # Display header
    header_line = "=" * 60
    print(header_line)
    print("Agent Bravo - Governance Proposal Processor".center(60))
    print(header_line)
    print()

    # --- Get Policy ---
    policy_info = get_voting_policy()
    policy = policy_info['policy']
    backstory = policy_info['backstory']

    # --- Get Proposals ---
    proposals = get_proposal_created_events()
    print(f"Total Proposals Found: {len(proposals)}")
    print()

    # --- Process Proposals ---
    for proposal in proposals:
        print(header_line)
        # Only show the last 4 digits of the proposalId prefixed with a "#"
        proposal_id_str = str(proposal['proposalId'])
        short_proposal_id = "#" + proposal_id_str[-4:]
        print(f"Processing Proposal ID: {short_proposal_id}".center(60))
        print(header_line)
        print(f"Description:\n{proposal['description']}")
        print("-" * 60)
        
        # --- Check Proposal Status ---
        status = get_proposal_status(proposal['proposalId'])
        print(f"Status: {status.upper()}")
        if status != 'active':
            # Yellow colored message for skipped proposals
            print("\033[93mSkipping proposal as it is not active.\033[0m")
            print(header_line + "\n")
            continue

        # --- Setup Agent Bravo Crew for Active Proposal ---
        agent_bravo = AgentBravoCrew()
        crew = agent_bravo.crew()
        inputs = {
            'proposal': proposal['description'],
            'policy': policy,
            'backstory': backstory
        }
        crew.kickoff(inputs=inputs)

        # --- Review Proposal and Make Decision ---
        gov_decision_dict = agent_bravo.review_task().output.to_dict()
        gov_decision = GovDecision(**gov_decision_dict)

        # --- Publish Decision to the Blockchain ---
        try:
            tx_receipt = publish_opinion_and_vote(gov_decision, proposal_id=proposal['proposalId'])
        except Exception as e:
            # Red colored error message
            print("\033[91m" + f"Error publishing decision to the blockchain: {e}" + "\033[0m")
            print(header_line + "\n")
            continue

        # --- Display Governance Decision Summary ---
        print("\n" + header_line)
        print("Governance Decision Summary".center(60))
        print(header_line)
        print(f"Opinion:\n{gov_decision.opinion}")
        print("-" * 60)
        print(f"Reasoning:\n{gov_decision.reasoning}")
        print("-" * 60)
        vote_str = 'AGAINST' if gov_decision.vote == 0 else 'FOR' if gov_decision.vote == 1 else 'ABSTAIN'
        print(f"Vote: {vote_str}")
        print(f"Transaction Hash: {tx_receipt['transactionHash'].hex() if tx_receipt else 'N/A'}")
        print(header_line + "\n")
        
    print("Agent Bravo execution has completed.\n")
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
