# AI Text to Speach File Reader

A terminal app that reads a file aloud using text-to-speech,
with optional LLM summarization powered by Ollama.

## Requirements

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)
- [Ollama](https://ollama.com/download) (if using --summarize)

## Setup

```bash
uv sync
ollama pull llama3.2:3b   # Only needed for --summarize
```

## Usage

```bash
# Read a file aloud
uv run src/main.py path/to/file.txt

# Summarize first, then read
uv run src/main.py path/to/file.txt --summarize

# Adjust speed
uv run src/main.py path/to/file.txt --rate 150