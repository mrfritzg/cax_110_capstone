import argparse 
from pathlib import Path
import pyttsx3
import ollama

def speak_text(text: str, rate: int = 175) -> None:
    """Uses pyttsx3 to speak the given text aloud."""
    engine = pyttsx3.init()
    engine.setProperty('rate', rate)
    engine.say(text)
    engine.runAndWait()

def read_file(file_path: str) -> str:
    """Reads the content of a file and returns it as a string."""
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    if not path.is_file():
        raise ValueError(f"The path {file_path} is not a file.")
    
    return path.read_text(encoding='utf-8')

def summarize_text(text: str, model: str = "llama3.2:3b") -> str:
    """Use a local LLM to summarize the given text."""
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

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description="Read a file aloud using AI file."
    )
    parser.add_argument(
        "file_path", 
        type=str, 
        help="The path to the file to be read."
    )
    parser.add_argument(
        "--rate", 
        type=int,
        default=175,
        help="The speech rate (default: 175 words per minute)."
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
    
    args = parser.parse_args()

    # Read the file and handle any exceptions
    try:
        content = read_file(args.file_path)

        if args.summarize:
            content = summarize_text(content, model=args.model)
            print("\nText successfully summarized")
            print(content)
            print("---\n")


        print("File content successfully read. Now passing it to AI for reading aloud...")
        print(f"The number of characters in the file: {len(content)}")
        print(f"Starting to read the file {args.file_path} aloud...")
        speak_text(content, rate=args.rate)
        print("------")
        print(content)  # For demonstration, we print the content. Replace with AI reading logic.
    except FileNotFoundError as e:
        print(f"Error: {e}")
        exit(1)
    except Exception as e:
        print(f"Unexpected error: {e}")
        exit(1)

if __name__ == "__main__":
    main()
