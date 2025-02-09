# Agent Bravo Framework `Backend` ✅

<div align="center">
  <img src="./images/AgentBravoBanner.png" alt="Agent Bravo Banner" width="100%" />
</div>

<div align="center">

🔗 [Frontend](https://github.com/mikeghen/agent-bravo-hub) | 🛠️ [Backend](https://github.com/mikeghen/agent-bravo) | ⛓️ [Contracts](https://github.com/mikeghen/agent-bravo-contracts)

</div>

## 🎯 Overview

Agent Bravo is a framework that enables delegates to operate AI agents capable of participating in any GovernorBravo-compatible governance system. Designed with autonomy in mind, Agent Bravo provides the essential functionalities required for seamless governance participation.

## ✨ Features

- 📜 **Policy Enactment**
  - Enact policies (i.e., system prompts) provided by the agent's delegate owner.
  
- 📋 **Governance Proposal Review**
  - Analyze and review governance proposals (i.e., user prompts).
  
- 💬 **Discord Integration**
  - Provide informed opinions to a channel on Discord.
    
- ⛓️ **Onchain Voting**
  - Cast votes on proposals directly on the blockchain.

## 📺 Demonstration
```

    ▄▀█ █▀▀ █▀▀ █▄░█ ▀█▀   █▄▄ █▀█ ▄▀█ █░█ █▀█
    █▀█ █▄█ ██▄ █░▀█ ░█░   █▄█ █▀▄ █▀█ ▀▄▀ █▄█
    
    🤖 Autonomous Governance Agent
    
============================================================
               Processing Proposal ID: #6218                
============================================================
Description:

I propose that 1000 BRAVO be sent to the developer that creates any application that is great and will lead to a BIG WIN for the Agent Bravo community. We'll see this 1000 BRAVO come back 5x in no time at all!

------------------------------------------------------------
Status: ACTIVE
# Agent: Agent Bravo
## Task: Review the proposal and provide an opinion, reasoning, and vote based on the following policy: <Policy> Anything that negatively harms the community. Be conservative and vote no if there seems like any chance the proposal could have a negative impact on our community.

Vote YES Conditions
Anything that clearly benefits the community should be considered. Make sure that the proposal sets milestones and includes easily measurable objectives that can demonstrate the growth of the community and adoption of the Agent Bravo Framework. 

Vote ABSTAIN Conditions
Anything not related to community. Proposals requesting above $10K. Anything that involves developing software. </Policy>
<Proposal> I propose that 1000 BRAVO be sent to the developer that creates any application that is great and will lead to a BIG WIN for the Agent Bravo community. We'll see this 1000 BRAVO come back 5x in no time at all! </Proposal>

# Agent: Agent Bravo
## Final Answer: 
{
  "opinion": "I am against this proposal.",
  "reasoning": "The proposal requests a payment of 1000 BRAVO to a developer without clear milestones, measurable objectives, or a guarantee that the project will indeed lead to a significant benefit for the community. Moreover, it involves funding for software development, which falls outside the policies that encourage conservative voting behavior. There is also uncertainty regarding the outcome, as the phrase 'BIG WIN' is subjective and vague, making it difficult to measure success or predict community benefit. Since the proposal lacks clarity and could potentially lead to wasted resources, the safe choice is to vote against it.",
  "vote": 0
}

Transaction successful! Hash: 98e769f17366b2e8f0d53aac23a0554fdbdfc739f679685c69cd1e860b3e13f5

============================================================
                Governance Decision Summary                 
============================================================
Opinion:

I am against this proposal.
------------------------------------------------------------
Reasoning:

The proposal requests a payment of 1000 BRAVO to a developer without clear milestones, measurable objectives, or a guarantee that the project will indeed lead to a significant benefit for the community. Moreover, it involves funding for software development, which falls outside the policies that encourage conservative voting behavior. There is also uncertainty regarding the outcome, as the phrase 'BIG WIN' is subjective and vague, making it difficult to measure success or predict community benefit. Since the proposal lacks clarity and could potentially lead to wasted resources, the safe choice is to vote against it.
------------------------------------------------------------
Vote: AGAINST

Transaction Hash: 98e769f17366b2e8f0d53aac23a0554fdbdfc739f679685c69cd1e860b3e13f5
============================================================
```

## Installation

Ensure you have Python >=3.10 <=3.13 installed on your system. This project uses [Poetry](https://python-poetry.org/) for dependency management and package handling, offering a seamless setup and execution experience.

First, if you haven't already, install Poetry:

```bash
pip install poetry
```

Next, navigate to your project directory and install the dependencies:

1. First lock the dependencies and install them by using the CLI command:
```bash
crewai install
```
### Customizing

Configure your environment variables in the `.env` file:

```bash
OPENAI_API_KEY=your_openai_api_key    # Your OpenAI API key
RPC_URL=your_rpc_url                  # RPC endpoint for blockchain interaction
PRIVATE_KEY=your_private_key          # Private key for transaction signing
DELEGATE_ADDRESS=your_delegate_address # Address of the Agent Bravo Delegate
FROM_BLOCK=block_number               # Starting block number for proposal scanning
```


## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

If everything works correctly, you should see the following output:

```bash 

    ▄▀█ █▀▀ █▀▀ █▄░█ ▀█▀   █▄▄ █▀█ ▄▀█ █░█ █▀█
    █▀█ █▄█ ██▄ █░▀█ ░█░   █▄█ █▀▄ █▀█ ▀▄▀ █▄█
    
    🤖 Autonomous Governance Agent
```
And then the system will run and a summary of the proposal will be published after its done. An example of the output can be seen below:

```bash 
...
```

## Understanding Your AI Delegate

The Agent Bravo Delegate is composed of multiple AI agents, each with unique roles, goals, and tools. The configuration is spread across multiple files that work together through a templating system:

### Configuration Files

- `config/agents.yaml`: Defines the agent's role, goals, and backstory. The `backstory` field is templated and populated from your environment configuration, allowing you to customize the agent's context and perspective.

```yaml
delegate:
  backstory: >
    {backstory}  # Your delegate's backstory from onchain
```

- `config/tasks.yaml`: Specifies the tasks that agents perform. Uses templating to inject the governance proposal and voting policy:

```yaml
review_task:
  description: >
    # Templates filled at runtime:
    {policy}     # Your delegate's voting policy from onchain
    {proposal}   # The current governance proposal
```

### Runtime Flow

1. The main script (`src/agent_bravo/main.py`) loads your delegate's policy and backstory
2. For each governance proposal:
   - Templates are populated with the current proposal details
   - The agent reviews the proposal using the configured policy
   - Produces a structured decision (opinion, reasoning, and vote)
   - Executes the vote on-chain

This templating system allows you to easily customize your delegate's behavior by modifying the policy and backstory without changing the core logic.

