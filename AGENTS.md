# Guidelines for Automated Agents

This file contains instructions for assistants working with this repository. Follow these guidelines when creating pull requests or running code.

## Repository Overview

The repository has been reorganized into standalone demos for each framework. Everything lives under `src/`:

- **autogen/** – Autogen AgentChat demos such as `agent_as_tool_demo.py`, `parallel_tools_demo.py`, `selector_group_chat_demo.py`, `swarm_agents_demo.py`, and other coordination experiments.
- **agents_sdk/** – Examples using the [openai-agents](https://pypi.org/project/openai-agents/) SDK.
- **swarm/** – Experiments with OpenAI's Swarm package, including human-in-the-loop handoffs and routines.

The repo does not include automated tests. Sample scripts serve as runnable examples and as references for building new experiments.

## Setup Instructions

1. Use **Python 3.10+**.
2. Install dependencies (Autogen AgentChat, `autogen-ext`, Azure SDKs, dotenv, etc.) using the refreshed requirements file:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the repository root and define your API key(s). At minimum:
   ```sh
   OPENAI_API_KEY=your_key_here
   ```
   Azure demos additionally require `API_KEY`, `DEPLOYMENT_NAME`, `ENDPOINT`, `MODEL`, and `API_VERSION`.

## Running Examples

After installation you can run any of the sample scripts. Common entry points include:

```sh
python src/autogen/sample.py                        # Lazy assistant with user handoffs
python src/autogen/agent_as_tool_demo.py            # Agent-as-tool pattern in Autogen
python src/autogen/swarm_agents_demo.py             # Azure Swarm demo with rich tooling
python src/autogen/reasoning_model_selector_demo.py # Routes tasks to different reasoning models
python src/agents_sdk/sample.py                     # OpenAI Agents SDK walkthrough
python src/swarm/sample.py                          # Minimal Swarm routine
python src/swarm/handoff.py                         # Human handoff Swarm scenario
python src/swarm/routine.py                         # Routine-based Swarm workflow
```

Review the source of each script for framework-specific configuration. Demos may contact external services depending on the credentials supplied.

## Development Conventions

- Keep code **PEP 8 compliant** and use clear, descriptive names.
- Add docstrings to new modules, classes, and functions.
- Prefer standard library modules over additional dependencies when practical.
- Place new examples alongside similar demos in `src/` (Autogen scripts under `autogen/`, Agents SDK under `agents_sdk/`, Swarm workflows under `swarm/`).
- Commit messages should be concise but informative (e.g. `Add Azure handoff swarm demo`).

## Testing

The project currently has no formal tests, but run `pytest` after changes to confirm there are no errors:
```sh
pytest -q
```
Also execute any example scripts you modify to ensure they still run end-to-end with the expected credentials.
