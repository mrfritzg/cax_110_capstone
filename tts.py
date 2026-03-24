"""
tts.py — Text-to-Speech module using the Kokoro AI model.

Responsibilities:
  - Load the Kokoro pipeline
  - Convert text to audio
  - Play audio through speakers
  - Optionally save audio to a .wav file

This module is intentionally separate from main.py.
Each file should have ONE clear job — this is called Separation of Concerns.
"""

import numpy as np
import sounddevice as sd
import soundfile as sf
from kokoro import KPipeline

# ── Voice Options ─────────────────────────────────────────────────────────────
# af = American Female | am = American Male
# bf = British Female  | bm = British Male

VOICES = {
    "af_heart":   "American Female - Heart (warm, natural) ⭐ recommended",
    "af_sarah":   "American Female - Sarah (clear, professional)",
    "af_nicole":  "American Female - Nicole (soft)",
    "af_sky":     "American Female - Sky (bright)",
    "am_adam":    "American Male - Adam (deep, clear)",
    "am_michael": "American Male - Michael (neutral)",
    "bf_emma":    "British Female - Emma",
    "bm_george":  "British Male - George",
}

# ── Pipeline Loader ───────────────────────────────────────────────────────────
def load_pipeline(lang: str = 'a') -> KPipeline:
    """
    Create and return a Kokoro TTS pipeline.

    Args:
        lang: Language code. 'a' = American English, 'b' = British English.

    Returns:
        A KPipeline object ready to generate audio.
    """
    print("Loading Kokoro TTS model (the first run may take a moment)...")
    return KPipeline(lang_code=lang)

# ── Main Text-to-Speech Function ─────────────────────────────────────────────────
def text_to_speech(
    text: str,
    voice: str = 'af_heart',
    speed: float = 1.0,
    save_path: str | None = None
) -> None:
    """
    Convert text to speech using Kokoro, play it and optionally save it.

    Args:
        text: The input text to be spoken.
        voice: The Kokoro voice to use (default: 'af_heart'). See VOICES dict for options.
        speed: Speech speed multiplier (default: 1.0 = Normal, 0.8 = Slower, 1.2 = Faster).
        save_path: Optional path to save the audio as a .wav file.
    """
    # Validate the voice is recognized
    if voice not in VOICES:
        print(f"Warning: Unknown voice '{voice}'. Falling back to 'af_heart'.")
        print("Run with --list-voices to see valid options.")
        voice = 'af_heart'  # Default to a known voice

   # Load the pipeline
    pipeline = load_pipeline()
    print(f"Generating audio with voice '{voice}' at speed {speed}x...")

    generator = pipeline(text, voice=voice, speed=speed)

    # Collect audio chunks and concatenate them if we need to save for later
    all_audio_chunks = []

    for i, (graphemes, phonemes, audio) in enumerate(generator):
        print(f" [chunk {i + 1}] Graphemes: {graphemes[:60]}...")
        all_audio_chunks.append(audio)

    # Play this chunk immediately as it is generated
    sd.play(audio, samplerate=24000)
    # Wait until audio finishes before continuing
    sd.wait()

    #Optionally save the full audio to a combined .wav file
    if save_path and all_audio_chunks:
        combined_audio = np.concatenate(all_audio_chunks)
        sf.write(save_path, combined_audio, 24000)
        print(f"Audio saved to {save_path}")

# ── Utility ───────────────────────────────────────────────────────────────────

def list_voices() -> None:
    """Print the available Kokoro voices."""
    print("\nAvailable Kokoro Voices:")
    print("-" * 50)
    for name, description in VOICES.items():
        print(f"  {name:<15} {description}")
    print()