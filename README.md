# Agent Bravo

Agent Bravo is a framework that enables delegates to operate AI agents capable of participating in any GovernorBravo-compatible governance system. Designed with autonomy in mind, Agent Bravo provides the essential functionalities required for seamless governance participation.

## Features

- **Policy Enactment**
  - Enact policies (i.e., system prompts) provided by the agent's delegate owner.
  
- **Governance Proposal Review**
  - Analyze and review governance proposals (i.e., user prompts).
  
- **Discord Integration**
  - Provide informed opinions to a channel on Discord.
    
- **Onchain Voting**
  - Cast votes on proposals directly on the blockchain.

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

**Add your `OPENAI_API_KEY` into the `.env` file**

- Modify `src/agent_bravo/config/agents.yaml` to define your agents
- Modify `src/agent_bravo/config/tasks.yaml` to define your tasks
- Modify `src/agent_bravo/crew.py` to add your own logic, tools and specific args
- Modify `src/agent_bravo/main.py` to add custom inputs for your agents and tasks

## Running the Project

To kickstart your crew of AI agents and begin task execution, run this from the root folder of your project:

```bash
$ crewai run
```

This command initializes the agent-bravo Crew, assembling the agents and assigning them tasks as defined in your configuration.

This example, unmodified, will run the create a `report.md` file with the output of a research on LLMs in the root folder.

## Understanding Your Crew

The agent-bravo Crew is composed of multiple AI agents, each with unique roles, goals, and tools. These agents collaborate on a series of tasks, defined in `config/tasks.yaml`, leveraging their collective skills to achieve complex objectives. The `config/agents.yaml` file outlines the capabilities and configurations of each agent in your crew.

## Support

For support, questions, or feedback regarding the AgentBravo Crew or crewAI.
- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
