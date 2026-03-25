"""
main.py — AI File Reader
Terminal app that reads a file aloud using Kokoro TTS and optional Ollama LLM.

Usage:
  uv run src/main.py report.txt
  uv run src/main.py report.txt --voice am_adam --speed 0.9
  uv run src/main.py report.txt --summarize
  uv run src/main.py report.txt --save output.wav
  uv run src/main.py --list-voices
"""

import argparse 
from pathlib import Path
import pyttsx3
import ollama
from tts import text_to_speech, list_voices

import warnings

# Suppress non-critical warnings from dependencies
warnings.filterwarnings('ignore', category=UserWarning, module='torch.nn.modules.rnn')
warnings.filterwarnings('ignore', category=FutureWarning, module='torch.nn.utils.weight_norm')

def speak_text(text: str, rate: int = 175) -> None:
    """Uses pyttsx3 to speak the given text aloud."""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

# ── File Reading ──────────────────────────────────────────────────────────────
def read_file(file_path: str) -> str:
    """Reads the content of a file and returns it as a string."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not path.is_file():
        raise ValueError(f"The path {file_path} is not a file.")
    
    return path.read_text(encoding='utf-8')

# ── LLM Summarization ─────────────────────────────────────────────────────────
def summarize_text_with_llm(text: str, model: str = "llama3.2:3b") -> str:
    """Use a local Ollama LLM to summarize the text before speaking it."""
    print(f"Sending the text to the LLM model '{model}' for summarization...")

    response = ollama.chat(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant. Summarizes the following text clearly, concisely, "
            "and informatively, keeping it under 200 words."},
            {"role": "user", "content": text}
        ]
    )
    return response["message"]["content"]

# ── CLI Entry Point ───────────────────────────────────────────────────────────
def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="AI File Reader — reads files aloud using Kokoro TTS",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  uv run src/main.py report.txt
  uv run src/main.py report.txt --voice am_adam --speed 0.9
  uv run src/main.py report.txt --summarize
  uv run src/main.py report.txt --save output.wav
  uv run src/main.py --list-voices
        """
    )

    # Positional argument (no -- prefix = required by default)
    # nargs="?" means "zero or one" — we handle the missing case manually
    parser.add_argument(
        "file_path", 
        type=str,
        nargs="?", 
        help="The path to the file to be read."
    )
    
    # Optional arguments
    # parser.add_argument(
    #     "--rate", 
    #     type=int,
    #     default=175,
    #     help="The speech rate (default: 175 words per minute)."
    # )

    parser.add_argument(
        "--voice",
        default="af_heart",
        help="Kokoro voice to use (default: af_heart)"
    )
    parser.add_argument(
        "--speed",
        type=float,
        default=1.0,
        help="Speech speed: 0.8=slow, 1.0=normal, 1.2=fast (default: 1.0)"
    )  
    parser.add_argument(
        "--summarize", 
        action="store_true",
        help="If set, the program will summarize the text before reading it aloud."
    )
    parser.add_argument(
        "--model",
        type=str,
        default="llama3.2:3b",
        help="Ollama model to use for summarization (default: 'llama3.2:3b')."
    )
    parser.add_argument(
        "--save",
        metavar="output.wav",
        help="Save the generated audio to a .wav file"
    )
    parser.add_argument(
        "--list-voices",
        action="store_true",
        help="Show all available Kokoro voices and exit"
    )
    
    args = parser.parse_args()

    # Handle --list-voices (doesn't need a file)
    if args.list_voices:
        list_voices()
        return

    # All other commands need a file path
    if not args.file_path:
        parser.error("Please provide a file path. Example: uv run src/main.py myfile.txt")

    try:
        # Read the file and handle any exceptions
        content = read_file(args.file_path)
        print("File content successfully read")
        print(f"✓ Loaded: {args.file_path} ({len(content)} characters)")
        print(f"✓ Loaded: {args.file_path} ")
        print(f"Here is a print out of the file: {content}")

        # Optionally summarize with Ollama LLM
        if args.summarize:
            print("Now passing it to AI for Summarization...")
            content = summarize_text_with_llm(content, model=args.model)
            print("\nLLM Text successfully summarized")
            print(content)
            print("---\n")

        # Step 2: Convert to speech and play
        print("Now converting to speech with Kokoro TTS...")
        text_to_speech(
            text=content + "I will also print out a summarized version of the text below",
            voice=args.voice,
            speed=args.speed,
            save_path=args.save,
        )
        # Step 3: Summarize with Ollama LLM
        print(summarize_text_with_llm(content, model=args.model))
        print("✓ Done.")
        
        # print(f"Starting to read the file {args.file_path} aloud...")
        # speak_text(content, rate=args.rate)
        # print("------")
        # print(content)  # For demonstration, we print the content. Replace with AI reading logic.
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except ConnectionError:
        print("Error: Could not connect to Ollama. Is it running?")
        print("Start it with: ollama serve")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
