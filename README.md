# Agentic AI Calculator

A basic tool-calling AI agent built using Python, Llama 3.1, and Ollama. It interprets natural-language mathematical queries, selects the appropriate arithmetic tool, executes calculations using Python functions, and returns the results through an LLM interaction loop.

### Features
- Addition, subtraction, multiplication, and division.
- LLM-based tool selection and function calling.
- Local inference using Ollama and Llama 3.1.
- Iterative tool execution and response generation.

### Requirements
- Python 3.10+
- [Ollama](https://ollama.com/)
- Llama 3.1 model
- OpenAI Python SDK

### Setup

Install the Python dependency:

```bash
pip install -r requirements.txt
```

Download the model:

```bash
ollama pull llama3.1
```

### Run

```bash
python3 calculator_agent.py
```

### How It Works

The LLM interprets the user's query and selects an appropriate tool. Python executes the corresponding arithmetic function, and the result is returned to the LLM to generate the final response.
