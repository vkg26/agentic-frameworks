# Guidelines for Automated Agents

This file contains instructions for assistants working with this repository. Follow these guidelines when creating pull requests or running code.

## Repository Overview

`src/` contains example code demonstrating different agentic frameworks:

- **agents_sdk/** – Simple examples using the [openai-agents](https://pypi.org/project/openai-agents/) SDK.
- **autogen/** – Experiments built on Microsoft Autogen. Custom agents live in `autogen/custom_agents/`.
- **swarm/** – Experiments with OpenAI's "swarm" multi-agent package.

The repository does not include automated tests. Sample scripts serve as runnable examples.

## Setup Instructions

1. Use **Python 3.10+**.
2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the repository root and define your API key(s). At minimum:
   ```sh
   OPENAI_API_KEY=your_key_here
   ```
   If you use Azure OpenAI, also set `API_KEY`, `DEPLOYMENT_NAME`, `ENDPOINT` and `MODEL`.

## Running Examples

After installation you can run any of the sample scripts. For instance:
```sh
python src/agents_sdk/sample.py
python src/autogen/sample.py
```
The scripts in `src/autogen` assume valid API credentials and may contact external services.

## Development Conventions

- Keep code **PEP8 compliant** and use clear, descriptive names.
- Add docstrings to new modules, classes and functions.
- Where practical, prefer standard library modules over additional dependencies.
- When adding examples, place them in the appropriate folder under `src/`.
- Commit messages should be concise but informative (e.g. `Add new autogen arithmetic sample`).

## Testing

The project currently has no formal tests, but run `pytest` after changes to confirm there are no errors:
```sh
pytest -q
```
Also run any example scripts you modify to ensure they still execute.

