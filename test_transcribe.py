import whisper

AUDIO_PATH = "levitating.mp3"

print("Loading OpenAI Whisper model (small)...")
model = whisper.load_model("small", device="cuda")
print("Model loaded.")

result = model.transcribe(AUDIO_PATH, fp16=False)
print("Transcription result:")
print(result["text"]) 