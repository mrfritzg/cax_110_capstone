#test_kokoro.py
from kokoro import KPipeline
import soundfile as sf
import sounddevice as sd

# Step 1: Create a TTS pipeline
# 'a' = American English | 'b' = British English
pipeline = KPipeline(lang_code='a')

#Step2: Define your text and voice
text = "Hello, this is a test of the Kokoro TTS pipeline. I hope you can hear me clearly!"

#Step 3: Generate audio from text
# Kokoro returns a generator — it produces audio in chunks (one per sentence)
generator = pipeline(
    text,
    voice='af_heart', # American Female voice named "heart"
    speed=1.0,  # 1.0 = normal, 0.8 = slower, 1.2 = faster
)

# Step 4: Loop through chunks and save/play each one
for i, (graphemes, phonemes, audio) in enumerate(generator):
    # graphemes = the original text chunk
    # phonemes  = how Kokoro is pronouncing it
    # audio     = the raw audio data (a numpy array)

    output_file = f"test_output_{i}.wav"
    sf.write(output_file, audio, 24000)   # 24000 Hz = sample rate
    print(f"Saved chunk {i}: {output_file}")

    # Play it immediately
    sd.play(audio, samplerate=24000)
    sd.wait()   # Wait until audio finishes before continuing

print("Done!")