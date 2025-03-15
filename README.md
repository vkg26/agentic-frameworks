# Agentic Frameworks Exploration

## Overview
This repository is dedicated to exploring various agentic frameworks, starting with [Microsoft Autogen](https://github.com/microsoft/autogen). The primary intent behind this repo is to experiment with different frameworks, understand their capabilities, and compare their efficiency in various scenarios. This is an ongoing effort where I will be testing and documenting my findings over time.

If you're interested in collaborating, feel free to reach out!

## Installation

To set up the environment and get started with Autogen, follow these steps:

### Prerequisites
Ensure you have Python 3.10+ installed on your system. You can check your Python version using:
```sh
python --version
```

### Setting Up the Environment
1. **Clone the Repository:**
   ```sh
   git clone https://github.com/YOUR_GITHUB_USERNAME/agentic-frameworks.git
   cd agentic-frameworks
   ```

2. **Create a Virtual Environment (Recommended):**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install Dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

4. **Install Autogen:**
   ```sh
   pip install -U "autogen-agentchat" "autogen-ext[openai]"
   ```
   and, autogen studio
   ```sh
   pip install -U "autogenstudio"
   ```

5. **Set Up Environment Variables:**
   Create a `.env` file in the root directory and add your OpenAI API key or Azure API details:
   ```sh
   OPENAI_API_KEY=your_api_key_here
   ```
   If using Azure OpenAI:
   ```sh
   AZURE_OPENAI_API_KEY=your_api_key_here
   AZURE_OPENAI_ENDPOINT=your_endpoint_here
   ```

## Directory Structure
```
agentic-frameworks/
│── src/
│   ├── autogen/
│   │   ├── custom_agents/
│   │   │   ├── magentic_one.py
│   │   │   ├── sample.py
│   │   │   ├── sample_azure_client.py
│── .env
│── .gitignore
│── LICENSE
│── README.md
│── requirements.txt
```

## Current Progress
- ✅ Initial setup with Autogen
- ✅ Implemented a few sample agent scripts
- 🔄 Exploring more frameworks and refining comparisons

## Future Work
- Add more agentic frameworks for comparison
- Develop benchmark tests for evaluating framework performance
- Document findings and best practices

## Contributing
Contributions and collaborations are welcome! If you have ideas or want to explore agentic frameworks together, feel free to open an issue or reach out.

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

