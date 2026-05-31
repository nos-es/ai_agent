# AI Agent

A small Python CLI project that uses Google Gemini function calling to interact with a local workspace.

The agent can:

* list files and directories
* read file contents
* run Python files with optional arguments
* write or overwrite files

The project currently uses a simple calculator app as the working directory for testing the agent's file and code interaction.

## Tech Stack

* Python
* Google GenAI SDK
* python-dotenv
* uv

## Setup

Clone the repository:

```bash
git clone https://github.com/nos-es/ai_agent.git
cd ai_agent
```

Create a `.env` file and add your Gemini API key:

```env
GEMINI_API_KEY=your_api_key_here
```

Install dependencies:

```bash
uv sync
```

## Usage

Run the agent with a prompt:

```bash
uv run main.py "Explain the calculator project"
```

Enable verbose output:

```bash
uv run main.py "Run the calculator tests" --verbose
```

## Notes

This is a learning project focused on understanding how AI agents can use tools to inspect and work with code.

