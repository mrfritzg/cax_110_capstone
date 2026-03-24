import argparse 
from pathlib import Path
import pyttsx3

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
    
    args = parser.parse_args()

    # Read the file and handle any exceptions
    try:
        content = read_file(args.file_path)
        print("File content successfully read. Now passing it to AI for reading aloud...")
        print(f"The number of characters in the file: {len(content)}")
        print(f"Starting to read the file {args.file_path} aloud...")
        speak_text(content, rate=args.rate)
        print("------")
        print(content)  # For demonstration, we print the content. Replace with AI reading logic.
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
