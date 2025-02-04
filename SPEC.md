# Agent Bravo Specification

## Overview

Agent Bravo is a framework that enables delegates to operate AI agents capable of participating in any GovernorBravo-compatible governance system. Designed with autonomy in mind, Agent Bravo provides the essential functionalities required for seamless governance participation.

## Methodology
Agent Bravo will perform a sequence of tasks to participate in governance. The sequence of tasks is as follows:

1. Reviews a governance proposal and produces an _opinion_ with _reasoning_.
2. After a review, it posts its opinion to a channel on Discord.
3. Finally, it casts an onchain vote on the proposal.

Not all tasks require an AI action. 

### AI Steps
* Review a governance proposal and produce an opinion with reasoning.

### Hardcoded Steps
* Post an opinion to a channel on Discord.
* Cast an onchain vote on the proposal.

## Crew AI Setup
This can be a single agent and a single task for the review step. The output of the agent will be a JSON object with the following fields:

* `opinion`: The opinion of the agent.
* `reasoning`: The reasoning behind the opinion.
* `vote`: The vote of the agent (1 = for, 0 = against, -1 = abstain).

## Discord Setup
After the review step, take the output of the agent and post it to a channel on Discord using Python.

```python
def post_opinion(opinion: str, reasoning: str, vote: int):
    # This function will create a post in a channel on Discord.
    pass
```

## Onchain Setup
After the review step, take the output of the agent and cast an onchain vote on the proposal using web3.py.
```python
def cast_vote(vote: int):
    # This function will cast a vote on the proposal.
    pass
```

## Future Work
* Set up the agent to listen to the blockchain for new proposal events.
* Add search tools to the agent so it can pull context from the internet. 
    * Perhaps using a query that only queries a specific website (e.g., the governance forum, Snapshot, etc.)
* Add a tool that allows the agent to post to the governance forum.
    * There is a Discourse API but it does not look like DAOs enable it on their own forums.
* Add a tool that allows the agent to post to Snapshot.
