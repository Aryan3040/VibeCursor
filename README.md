# VibeBackend - Whisper Transcription Server

A lightweight FastAPI server that provides OpenAI Whisper transcription services for voice input applications, designed specifically for integration with Cursor's voice input feature.

## Features

- **FastAPI Server**: High-performance async web server
- **Whisper Integration**: OpenAI Whisper for accurate speech-to-text
- **GPU Acceleration**: CUDA support for faster transcription
- **CORS Support**: Cross-origin requests enabled for web integration
- **File Upload**: Accepts various audio formats
- **Error Handling**: Robust error handling and validation

## Quick Start

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended for faster processing)
- 4GB+ VRAM for optimal performance

### Installation

1. **Clone the repository:**
   ```bash
   git clone <your-repo-url>
   cd vibebackend
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the server:**
   ```bash
   python main.py
   ```

The server will start on `http://localhost:8000`

## API Endpoints

### Transcribe Audio
```http
POST /transcribe
Content-Type: multipart/form-data

file: [audio_file]
```

**Response:**
```json
{
  "text": "transcribed text content"
}
```

### Health Check
```http
GET /
```

**Response:**
```json
{
  "message": "Voice Assistant Transcription Backend is running."
}
```

## How It Works

### Architecture

- **FastAPI**: Modern, fast web framework for building APIs
- **Whisper Model**: OpenAI's speech recognition model (small variant)
- **CUDA Acceleration**: GPU-accelerated transcription processing
- **File Handling**: Temporary file management for audio processing

### Processing Pipeline

1. **File Upload**: Accept audio file via multipart form data
2. **Temporary Storage**: Save file to temporary location
3. **Transcription**: Process audio with Whisper model
4. **Cleanup**: Remove temporary file
5. **Response**: Return transcribed text

## File Structure

```
vibebackend/
├── main.py              # FastAPI server
├── test_transcribe.py   # Testing script
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Usage Examples

### Python Client

```python
import requests

# Transcribe audio file
with open('audio.wav', 'rb') as f:
    files = {'file': f}
    response = requests.post('http://localhost:8000/transcribe', files=files)
    
if response.status_code == 200:
    result = response.json()
    print(f"Transcription: {result['text']}")
else:
    print(f"Error: {response.text}")
```

### JavaScript Client

```javascript
// Transcribe audio file
const transcribeAudio = async (audioFile) => {
  const formData = new FormData();
  formData.append('file', audioFile);
  
  const response = await fetch('http://localhost:8000/transcribe', {
    method: 'POST',
    body: formData
  });
  
  if (response.ok) {
    const result = await response.json();
    return result.text;
  } else {
    throw new Error('Transcription failed');
  }
};

// Usage
const fileInput = document.getElementById('audioFile');
fileInput.addEventListener('change', async (e) => {
  const file = e.target.files[0];
  try {
    const transcription = await transcribeAudio(file);
    console.log('Transcription:', transcription);
  } catch (error) {
    console.error('Error:', error);
  }
});
```

### cURL Example

```bash
curl -X POST "http://localhost:8000/transcribe" \
     -H "accept: application/json" \
     -H "Content-Type: multipart/form-data" \
     -F "file=@audio.wav"
```

## Configuration

### Server Settings

- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: `8000` (configurable)
- **CORS**: Enabled for all origins

### Whisper Configuration

```python
# In main.py, modify these settings:
model = whisper.load_model("small", device="cuda")  # Change model size
# Available models: "tiny", "base", "small", "medium", "large"
```

### Customization

- **Model Size**: Change Whisper model for different accuracy/speed trade-offs
- **Device**: Switch between "cuda" and "cpu" based on hardware
- **CORS Settings**: Configure allowed origins for production deployment

## Troubleshooting

### Common Issues

1. **CUDA out of memory**:
   - Use smaller Whisper model ("tiny" or "base")
   - Switch to CPU processing: `device="cpu"`
   - Close other GPU applications

2. **File upload errors**:
   - Check file format (supports: wav, mp3, m4a, flac)
   - Ensure file size is reasonable (< 100MB)
   - Verify file is not corrupted

3. **Slow transcription**:
   - Use GPU acceleration if available
   - Consider smaller Whisper model
   - Process shorter audio files

### Performance Tips

- **GPU Memory**: Ensure sufficient VRAM for Whisper model
- **Model Selection**: 
  - `tiny`: Fastest, lowest accuracy
  - `base`: Good balance
  - `small`: Better accuracy (default)
  - `medium/large`: Best accuracy, slowest
- **Batch Processing**: Process multiple files sequentially

## Deployment

### Development
```bash
python main.py
```

### Production with Uvicorn
```bash
pip install uvicorn
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 1
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Security Considerations

### Production Deployment

- **CORS Configuration**: Restrict allowed origins
- **Rate Limiting**: Implement request rate limiting
- **Authentication**: Add API key authentication
- **File Validation**: Validate file types and sizes
- **HTTPS**: Use SSL/TLS encryption

### Example Security Configuration

```python
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import APIKeyHeader

API_KEY_HEADER = APIKeyHeader(name="X-API-Key")

def verify_api_key(api_key: str = Depends(API_KEY_HEADER)):
    if api_key != "your-secret-key":
        raise HTTPException(status_code=403, detail="Invalid API key")
    return api_key

@app.post("/transcribe")
async def transcribe_audio(
    file: UploadFile = File(...),
    api_key: str = Depends(verify_api_key)
):
    # ... transcription logic
```

## Testing

### Run Test Script
```bash
python test_transcribe.py
```

### Manual Testing
```bash
# Test with curl
curl -X POST "http://localhost:8000/transcribe" \
     -F "file=@test.wav"

# Test health endpoint
curl "http://localhost:8000/"
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) for speech recognition
- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Cursor](https://cursor.sh/) for the voice input inspiration

## Future Enhancements

- [ ] Multiple language support
- [ ] Real-time streaming transcription
- [ ] Audio preprocessing options
- [ ] Batch processing endpoint
- [ ] Model fine-tuning support
- [ ] WebSocket support for live transcription
- [ ] Audio format conversion
- [ ] Transcription confidence scores 