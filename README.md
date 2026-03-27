# AI Text to Speech Reader & Summarizer

This app will be an educational tool to aid people with Dyslexia and
An app that uses Koroko LLM Model to read files/text aloud using text-to-speech (TTS),
with LLM summarization powered by Ollama LLM.

This version of the app is a CLI version that will:
1. Accept a file path from the terminal
2. Read the file
3. Summarize with Ollama LLM
4. **Convert text to natural-sounding AI speech using Kokoro**
5. Play the audio aloud


## Requirements

> - Python 3.11+
> - [uv](https://docs.astral.sh/uv/)
> - [Ollama](https://ollama.com/download) (if using --summarize)
> - Koroko-82M TTS LLM https://huggingface.co/hexgrad/Kokoro-82M Kokoro is an open-weight TTS model with 82 million parameters.
> - `soundfile` — reads and writes `.wav` audio files
> - `sounddevice` — plays audio through your speakers from Python
> - `numpy` — used to combine audio chunks into one playback stream

## Setup

```bash
uv sync
ollama pull llama3.2:3b   # Only needed for --summarize
uv add kokoro soundfile sounddevice numpy
```

## Usage

```bash
# Read the file with default voice
uv run src/main.py test.txt

# Try a different voice
uv run src/main.py test.txt --voice am_adam

# Try slower speed
uv run src/main.py test.txt --speed 0.85

# Save audio to a file
uv run src/main.py test.txt --save my_reading.wav


### Project File Structure

```
file-reader/
├── pyproject.toml       ← uv manages this (don't edit manually)
├── README.md            ← how to install and run your app
├── test.txt             ← test input file
├── my_reading.wav       ← generated audio (add to .gitignore)
├── main.py          ← CLI entry point — handles args, file, LLM
└── tts.py           ← TTS module — handles Kokoro audio generation
```

### 1. Install `espeak-ng` (Required by Kokoro)

Kokoro uses `espeak-ng` under the hood to convert text into phonemes (sound units).

**macOS:**
```bash
brew install espeak-ng
```

**Ubuntu/Debian Linux:**
```bash
sudo apt-get install espeak-ng
```

**Windows:**
- Download the installer from: https://github.com/espeak-ng/espeak-ng/releases
- Look for a file like `espeak-ng-20191129-b702b03-x64.msi`
- Install it, then restart your terminal

**Verify it works:**
```bash
espeak-ng "hello world"
# You should hear a robotic voice say "hello world"
```

---



### STEP 1 — Add Kokoro to Your Project

In your existing `file-reader` project folder:

```bash
uv add kokoro soundfile sounddevice numpy
```

> **What these do:**
> - `kokoro` — the Kokoro TTS AI model library
> - `soundfile` — reads and writes `.wav` audio files
> - `sounddevice` — plays audio through your speakers from Python
> - `numpy` — used to combine audio chunks into one playback stream

**Verify the install worked:**
```bash
uv run python -c "from kokoro import KPipeline; print('Kokoro installed OK!')"
```

---