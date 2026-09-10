# JARVIS - Personal AI Assistant for Windows 10

> A fully functional, production-ready AI assistant running in Python IDLE with speech recognition, text-to-speech, and advanced OS automation. Powered by Google Gemini 2.5 Flash or OpenAI GPT-4o.

![Python](https://img.shields.io/badge/Python-3.8+-blue?logo=python)
![Windows](https://img.shields.io/badge/Windows-10+-0078D4?logo=windows)
![License](https://img.shields.io/badge/License-MIT-green)
![AI](https://img.shields.io/badge/AI-Gemini%2FGPT--4o-orange)

---

## ✨ Features

### 🧠 AI Intelligence
- **Google Gemini 2.5 Flash** (Free, recommended for beginners)
- **OpenAI GPT-4o** (Most capable, requires API credits)
- Intelligent context-aware conversations
- Natural language understanding
- Witty and conversational responses

### 🎤 Audio I/O
- **Speech-to-Text (STT):** Google Speech Recognition (no API key needed)
- **Text-to-Speech (TTS):** pyttsx3 with British male voice
- Real-time microphone input
- Clear audio feedback

### 🖥️ System Control
- **Application Launcher:** Open 15+ Windows applications
- **Web Navigation:** Open websites, perform Google searches
- **Audio Control:** Volume, mute, unmute
- **Display Control:** Brightness adjustment
- **System Control:** Lock screen, sleep mode
- **Media Control:** Play, pause, skip tracks

### 🛡️ Reliability
- Comprehensive error handling
- Graceful fallbacks
- Detailed logging system
- IDLE-compatible (no GUI framework conflicts)
- Production-ready architecture

### 🎯 Flexible Modes
- **Voice Mode:** Hands-free operation with speech recognition
- **Text Mode:** Keyboard input for testing or quiet environments
- **Launcher UI:** Interactive menu for backend and mode selection

---

## 🚀 Quick Start

### 1️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 2️⃣ Get Your API Key

**Choose Gemini (Free & Recommended):**
```bash
# Visit: https://ai.google.dev/
# Get your free API key
set GOOGLE_API_KEY=your_key_here
```

**Or Choose OpenAI (Paid but Most Capable):**
```bash
# Visit: https://platform.openai.com/api-keys
# Get your API key
set OPENAI_API_KEY=your_key_here
```

### 3️⃣ Launch JARVIS
```bash
python launcher.py
```

---

## 📖 Usage Guide

### Voice Command Examples

```
"JARVIS, open Chrome"              # Launch web browser
"JARVIS, visit YouTube"             # Navigate to website
"JARVIS, search for Python"         # Google search
"JARVIS, open WhatsApp"             # Launch messenger
"JARVIS, set volume to 50"          # Control volume
"JARVIS, set brightness to 80"      # Adjust display
"JARVIS, mute audio"                # Mute system
"JARVIS, play music"                # Media control
"JARVIS, next track"                # Skip song
"JARVIS, lock the screen"           # Security
"JARVIS, tell me a joke"            # General query
"JARVIS, what's the weather?"       # Information
"JARVIS, exit"                      # Shutdown
```

### Text Mode (Keyboard Input)

Perfect for testing or quiet environments:
```
[You]: open Spotify
[JARVIS]: Opening Spotify...

[You]: set volume to 75
[JARVIS]: Volume set to 75%

[You]: exit
```

---

## 📋 System Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    JARVIS Main Class                     │
│         (Orchestrates all components)                    │
└──────────────────────┬──────────────────────────────────┘
                       │
        ┌──────────────┼──────────────┐
        │              │              │
        ▼              ▼              ▼
   ┌──────────┐  ┌──────────┐  ┌──────────┐
   │AudioIn   │  │Brain     │  │OSControl │
   │(STT)     │  │(AI)      │  │(Hands)   │
   └──────────┘  └──────────┘  └──────────┘
        │              │              │
        ▼              ▼              ▼
   Google STT   Gemini/GPT-4o   System APIs
   (Microphone)  (Intelligence)  (subprocess)
        │              │              │
        └──────────────┼──────────────┘
                       ▼
                  ┌──────────┐
                  │AudioOut  │
                  │(TTS)     │
                  └──────────┘
                   pyttsx3
                  (Speaker)
```

---

## 🔧 Configuration

Edit `jarvis_gemini.py` or `jarvis.py`:

```python
class Config:
    GEMINI_MODEL = "gemini-2.5-flash"  # AI model
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    SPEECH_TIMEOUT = 10                 # Mic listen timeout
    VOICE_RATE = 150                    # TTS speech speed
    VOICE_VOLUME = 0.9                  # TTS volume (0-1)
    
    DEBUG_MODE = True                   # Show debug messages
```

---

## 📦 Supported Applications

| Category | Applications |
|----------|---------------|
| **Browsers** | Chrome, Firefox, Edge |
| **Communication** | WhatsApp, Discord, Telegram, Slack |
| **Productivity** | Notepad, Word, Excel, PowerPoint, VSCode |
| **Media** | Spotify |
| **System** | Calculator, Terminal, PowerShell |

---

## 🔑 API Keys Setup

### Google Gemini (Free)

1. Go to [ai.google.dev](https://ai.google.dev/)
2. Click "Get API Key" → "Create API key in new project"
3. Copy the key
4. Set environment variable:
   ```cmd
   set GOOGLE_API_KEY=your_key_here
   ```

### OpenAI GPT-4o (Paid)

1. Go to [platform.openai.com](https://platform.openai.com/)
2. Navigate to [API Keys](https://platform.openai.com/api-keys)
3. Click "Create new secret key"
4. Copy the key (save securely)
5. Set environment variable:
   ```cmd
   set OPENAI_API_KEY=your_key_here
   ```

---

## 🐛 Troubleshooting

| Issue | Solution |
|-------|----------|
| **Module not found** | `pip install -r requirements.txt` |
| **API key not found** | Set environment variable in Windows |
| **Microphone not working** | Check Windows Settings → Privacy → Microphone |
| **Speech recognition timeout** | Speak louder and clearer |
| **PyAudio installation fails** | `pip install pipwin` then `pipwin install PyAudio` |
| **Application won't open** | Verify app is installed and in PATH |
| **No audio output** | Check Windows volume and speakers |

---

## 💻 System Requirements

- **OS:** Windows 10 or later
- **Python:** 3.8 or higher
- **RAM:** 2GB minimum (4GB recommended)
- **Storage:** ~500MB for dependencies
- **Internet:** Required for API calls
- **Microphone:** Optional (for voice mode)

---

## 🎓 Architecture Details

### Audio Engine (Ear & Voice)
- **STT:** Captures microphone input → Converts to text
- **TTS:** Converts responses to audio → Plays through speakers
- Includes noise adjustment and error handling

### Brain (Intelligence)
- Integrates with Gemini 2.5 Flash or GPT-4o
- Maintains conversation history (context-aware)
- Parses user intent to trigger system actions
- Intelligent function calling for OS automation

### OS Control Engine (The Hands)
- Direct system API access via subprocess
- Application launcher/closer
- Audio/display/media controls
- Website navigation
- Media playback control

---

## 🔐 Security Notes

1. **API Keys:** Store securely in environment variables
2. **Never hardcode credentials** in source files
3. **Use HTTPS** for web navigation
4. **Limit microphone permissions** to trusted applications
5. **Review system actions** before execution in production

---

## 📝 Example Use Cases

### 1. Hands-Free Computing
```
"Open my IDE and start a new project"
→ Launches VSCode, ready for development
```

### 2. Smart Workflow
```
"Search Stack Overflow for async Python"
→ Opens browser with search results
```

### 3. Media Entertainment
```
"Play my Spotify playlist and set volume to 75"
→ Launches Spotify and adjusts volume
```

### 4. System Management
```
"Lower brightness to 50 and lock screen"
→ Adjusts display and secures workstation
```

---

## 🚀 Advanced Features

### Multi-Backend Support
Switch between Gemini and GPT-4o seamlessly:
```bash
python launcher.py  # Interactive menu
```

### Conversation Memory
JARVIS remembers previous exchanges:
```
You: "What's Python?"
JARVIS: "[Explanation]"

You: "Can you give me an example?"
JARVIS: "[Example related to Python]"  ← Context-aware
```

### Error Recovery
Automatic fallback mechanisms:
- Microphone error → Continue listening
- API error → Graceful message and retry
- Speech recognition failure → Prompt for clarity

---

## 📊 Performance

- **Response Time:** <2 seconds (API-dependent)
- **CPU Usage:** <5% at idle
- **Memory Usage:** ~200MB
- **Latency:** Minimal with local processing

---

## 🌐 Offline Capabilities

Some features work offline:
- ✅ Text-to-Speech (TTS)
- ✅ Application launching
- ✅ System controls
- ❌ Speech Recognition (requires internet)
- ❌ AI responses (requires API)

---

## 📚 File Structure

```
personal-ai-assistant/
├── jarvis_gemini.py          # Gemini 2.5 Flash implementation
├── jarvis.py                 # OpenAI GPT-4o implementation
├── launcher.py               # Interactive launcher menu
├── requirements.txt          # Python dependencies
├── SETUP_GUIDE.md           # Installation guide
├── README.md                # This file
└── .gitignore               # Git configuration
```

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

---

## 📄 License

MIT License - Feel free to use, modify, and distribute.

---

## 📞 Support & Resources

- **GitHub:** [personal-ai-assistant](https://github.com/ruannchriz10/personal-ai-assistant)
- **Gemini Docs:** [ai.google.dev](https://ai.google.dev/docs)
- **OpenAI Docs:** [platform.openai.com](https://platform.openai.com/docs)
- **SpeechRecognition:** [pypi.org/project/SpeechRecognition](https://pypi.org/project/SpeechRecognition/)

---

## 🎉 Getting Started

```bash
# Clone or download the repository
cd personal-ai-assistant

# Install dependencies
pip install -r requirements.txt

# Set your API key
set GOOGLE_API_KEY=your_key_here

# Launch JARVIS
python launcher.py
```

**Enjoy your personal AI assistant!** 🤖

---

## 📊 Comparison: Gemini vs GPT-4o

| Feature | Gemini 2.5 Flash | GPT-4o |
|---------|------------------|--------|
| **Cost** | Free | Paid |
| **API Key** | Easy to get | Requires subscription |
| **Speed** | Very fast | Fast |
| **Accuracy** | Excellent | Excellent |
| **Best For** | Beginners, testing | Production, advanced tasks |
| **Rate Limit** | Generous | Plan-dependent |
| **Learning** | Great for learning | Production use |

**Recommendation:** Start with Gemini for learning, move to GPT-4o for production.

---

## ✨ Tips for Best Performance

1. **Clear speech** - Speak naturally and clearly
2. **Quiet environment** - Minimize background noise
3. **Grant permissions** - Allow Python to access microphone
4. **Monitor quota** - Keep track of API usage
5. **Keep updated** - Regularly update dependencies
6. **Test locally** - Use text mode before voice mode

---

## 🚀 Roadmap

Future enhancements:
- [ ] Multi-language support
- [ ] Custom voice profiles
- [ ] Advanced function calling
- [ ] Mobile companion app
- [ ] Browser extension
- [ ] Enhanced web automation
- [ ] Calendar integration
- [ ] Email automation

---

**Built with ❤️ for Windows 10 | Python 3.8+**

*Last Updated: 2026-09-10*
