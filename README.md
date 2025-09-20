# Agentic Frameworks Exploration

## Overview

This repository explores modern agentic frameworks with a focus on [Autogen AgentChat](https://microsoft.github.io/autogen/), the OpenAI Agents SDK, and OpenAI's Swarm toolkit. After the recent refactor the examples have been reorganized into self-contained demos grouped by framework under `src/autogen/`, `src/agents_sdk/`, and `src/swarm/`, making it easier to compare approaches, reuse components, and experiment with different coordination patterns.

Each demo highlights a specific capability—tool use, human-in-the-loop handoffs, routing, or Azure-hosted agents—so you can quickly try ideas and extend them for your own projects.

## Installation

### Prerequisites

* Python 3.10 or newer
* An OpenAI or Azure OpenAI API key depending on the demo you plan to run

Verify your Python version with:

```sh
python --version
```

### Set up the project

1. **Clone the repository**

   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/agentic-frameworks.git
   cd agentic-frameworks
   ```

2. **(Optional) Create a virtual environment**

   ```sh
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install dependencies**

   The refreshed `requirements.txt` consolidates everything required for the demos, including Autogen AgentChat, Autogen extensions, Azure connectors, and supporting utilities.

   ```sh
   pip install -r requirements.txt
   ```

### Configure credentials

Create a `.env` file in the repository root so the demos can load credentials via `python-dotenv`:

```dotenv
OPENAI_API_KEY=your_openai_key

# Azure-specific demos (swarm_agents_demo.py, sample_azure_client.py)
API_KEY=your_azure_openai_key
DEPLOYMENT_NAME=your_deployment
MODEL=gpt-4o
ENDPOINT=https://your-resource.openai.azure.com/
API_VERSION=2024-06-01
```

Only the variables relevant to the demos you want to run are required. Refer to the source code for any additional environment flags.

## Directory Structure

```
agentic-frameworks/
├── src/
│   ├── autogen/
│   │   ├── agent_as_tool_demo.py
│   │   ├── arithmetic_agent.py
│   │   ├── model_context_demo.py
│   │   ├── parallel_tools_demo.py
│   │   ├── reasoning_model_selector_demo.py
│   │   ├── round_robin_team_with_user_proxy_agent.py
│   │   ├── sample.py
│   │   ├── sample_azure_client.py
│   │   ├── selector_group_chat_demo.py
│   │   └── swarm_agents_demo.py
│   ├── agents_sdk/
│   │   └── sample.py
│   └── swarm/
│       ├── handoff.py
│       ├── routine.py
│       └── sample.py
├── AGENTS.md
├── LICENSE
├── README.md
└── requirements.txt
```

## Running the demos

Each script is self-contained—activate your environment, export the required keys, and run whichever example you want to explore from the framework-specific subdirectories.

```sh
python src/autogen/sample.py                            # Lazy assistant that hands off to the user
python src/autogen/agent_as_tool_demo.py                # Showcases agents acting as tools inside Autogen
python src/autogen/parallel_tools_demo.py               # Demonstrates coordinated parallel tool execution
python src/autogen/reasoning_model_selector_demo.py     # Routes tasks to different reasoning models
python src/autogen/swarm_agents_demo.py                 # Azure Swarm demo with rich handoffs and tools
python src/autogen/model_context_demo.py                # Explores model context management patterns
python src/agents_sdk/sample.py                         # OpenAI Agents SDK example
python src/swarm/sample.py                              # Minimal Swarm workflow
python src/swarm/handoff.py                             # Swarm handoff with a human-in-the-loop
python src/swarm/routine.py                             # Routine-driven Swarm collaboration
```

Feel free to inspect other scripts in `src/` for additional scenarios such as selector group chats, Azure-hosted clients, and arithmetic-focused agents. When modifying or extending a demo, run it directly to confirm behaviour and iterate quickly.

## Current Progress

- ✅ Refactored the codebase into modular Autogen, Agents SDK, and Swarm demos
- ✅ Added richer tool-enabled scenarios, including Azure-hosted Swarm interactions
- ✅ Centralized dependencies (Autogen AgentChat, `autogen-ext`, Azure SDKs, etc.) in `requirements.txt`
- 🔄 Expanding coverage of decision-making and routing patterns
- 🔄 Documenting comparative learnings across frameworks

## Future Work

- Add benchmarking utilities to compare response quality, latency, and cost across frameworks
- Grow the library of multi-agent coordination templates (escalations, fallbacks, guardrails)
- Capture troubleshooting notes for Azure/OpenAI deployments and streaming UIs
- Publish write-ups summarizing lessons learned from each experiment

## Contributing

Contributions and collaborations are welcome! If you have ideas or want to explore agentic frameworks together, feel free to open an issue or reach out.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

