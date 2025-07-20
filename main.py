import os
import tempfile
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import shutil
import whisper

print("Loading OpenAI Whisper model (small)...")
model = whisper.load_model("small", device="cuda")
print("Model loaded.")

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    suffix = os.path.splitext(file.filename)[1]
    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
        temp_path = tmp.name
        try:
            shutil.copyfileobj(file.file, tmp)
        finally:
            file.file.close()
    try:
        result = model.transcribe(temp_path, fp16=False)
        transcription = result["text"].strip()
        return JSONResponse(content={"text": transcription})
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Transcription failed: {e}")
    finally:
        if os.path.exists(temp_path):
            os.remove(temp_path)

@app.get("/")
def root():
    return {"message": "Voice Assistant Transcription Backend is running."} 