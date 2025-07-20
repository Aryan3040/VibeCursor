# VibeBackend - Voice Input System with Frontend

A complete voice input system consisting of a FastAPI Whisper transcription server and a Tkinter frontend application for voice-controlled macros and text input.

## Features

- **FastAPI Server**: High-performance async web server for transcription
- **Whisper Integration**: OpenAI Whisper for accurate speech-to-text
- **GPU Acceleration**: CUDA support for faster transcription
- **Tkinter Frontend**: Desktop application for voice recording and macro automation
- **Macro Recording**: Record mouse clicks and keyboard shortcuts for automation
- **Voice-to-Text**: Real-time voice transcription with automatic text insertion
- **CORS Support**: Cross-origin requests enabled for web integration
- **Error Handling**: Robust error handling and validation

## Quick Start

### Prerequisites

- Python 3.8+
- CUDA-capable GPU (recommended for faster processing)
- 4GB+ VRAM for optimal performance
- Microphone access

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

3. **Run the backend server:**
   ```bash
   python main.py
   ```

4. **Run the frontend application:**
   ```bash
   python frontend.py
   ```

The server will start on `http://localhost:8000` and the frontend will open as a desktop application.

## System Architecture

### Backend (main.py)
- **FastAPI Server**: Handles audio file uploads and transcription requests
- **Whisper Model**: OpenAI's speech recognition model (small variant)
- **CUDA Acceleration**: GPU-accelerated transcription processing
- **File Handling**: Temporary file management for audio processing

### Frontend (frontend.py)
- **Tkinter GUI**: Modern desktop interface with dark theme
- **Voice Recording**: Real-time audio capture and processing
- **Macro System**: Record and replay mouse clicks and keyboard shortcuts
- **Text Automation**: Automatic text insertion via clipboard and macros

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

## Frontend Usage

### Recording Macros
1. Click "Record Macro" to start recording
2. Perform the actions you want to automate (mouse clicks, Ctrl+V)
3. Press 'S' to stop recording
4. The macro will be saved for future use

### Voice Input
1. Ensure a macro is recorded
2. Click "Listen" to start voice recording
3. Speak your text
4. Press Space to stop recording
5. The transcribed text will automatically be inserted using the recorded macro

### Emergency Stop
Press `Ctrl + Shift + Q` to immediately close the application.

## File Structure

```
vibebackend/
├── main.py              # FastAPI server
├── frontend.py          # Tkinter desktop application
├── test_transcribe.py   # Testing script
├── requirements.txt     # Python dependencies
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Configuration

### Server Settings

- **Host**: `0.0.0.0` (accessible from any IP)
- **Port**: `8000` (configurable)
- **CORS**: Enabled for all origins

### Frontend Settings

- **Server URL**: Configure in `frontend.py` line 21
- **Emergency Kill**: `Ctrl + Shift + Q` (configurable)
- **Theme**: Dark theme with purple/blue accent colors

### Whisper Configuration

```python
# In main.py, modify these settings:
model = whisper.load_model("small", device="cuda")  # Change model size
# Available models: "tiny", "base", "small", "medium", "large"
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
```

## Troubleshooting

### Common Issues

1. **CUDA out of memory**:
   - Use smaller Whisper model ("tiny" or "base")
   - Switch to CPU processing: `device="cpu"`
   - Close other GPU applications

2. **Frontend connection errors**:
   - Ensure the backend server is running
   - Check the SERVER_URL in frontend.py
   - Verify firewall settings

3. **Audio recording issues**:
   - Check microphone permissions
   - Ensure audio drivers are installed
   - Test with different audio devices

4. **Macro playback problems**:
   - Ensure target applications are in focus
   - Check if applications block automation
   - Verify screen resolution hasn't changed

### Performance Tips

- **GPU Memory**: Ensure sufficient VRAM for Whisper model
- **Model Selection**: 
  - `tiny`: Fastest, lowest accuracy
  - `base`: Good balance
  - `small`: Better accuracy (default)
  - `medium/large`: Best accuracy, slowest
- **Audio Quality**: Use good microphone for better transcription accuracy

## Deployment

### Development
```bash
# Terminal 1: Backend
python main.py

# Terminal 2: Frontend
python frontend.py
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

### Frontend Security

- **Local Access**: Frontend only connects to localhost by default
- **No Data Storage**: No sensitive data is stored locally
- **Emergency Stop**: Built-in kill switch for security

## Testing

### Backend Testing
```bash
python test_transcribe.py
```

### Frontend Testing
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
- [Tkinter](https://docs.python.org/3/library/tkinter.html) for the GUI
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
- [ ] Custom macro file format
- [ ] Cloud synchronization
- [ ] Voice command recognition 