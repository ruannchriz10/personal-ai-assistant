# JARVIS - Personal AI Assistant Setup Guide

## 🚀 Quick Start

### Prerequisites
- **Windows 10** (or later)
- **Python 3.8+** ([Download here](https://www.python.org/downloads/))
- **Microphone** (optional, for voice mode)
- **Internet Connection** (for API calls)

---

## 📦 Step 1: Install Dependencies

### Option A: Automated Installation (Recommended)

Open Command Prompt and run:

```cmd
pip install -r requirements.txt
```

### Option B: Manual Installation

```cmd
pip install google-generativeai
pip install openai
pip install SpeechRecognition
pip install pyttsx3
pip install PyAudio
pip install python-dotenv
```

> **Note for PyAudio issues on Windows:**
> If PyAudio installation fails, try:
> ```cmd
> pip install pipwin
> pipwin install PyAudio
> ```

---

## 🔑 Step 2: Get Your API Key

### Choose One Backend (or Both):

#### **Option 1: Google Gemini 2.5 Flash (Recommended for Beginners)**

✅ **FREE** with generous rate limits
✅ No credit card required
✅ Great for development and testing

1. Go to [AI Studio](https://ai.google.dev/)
2. Click "Get API Key"
3. Select "Create API key in new project"
4. Copy your API key

**Set Environment Variable (Windows):**

**Method A - Temporary (Current Session Only):**
```cmd
set GOOGLE_API_KEY=your_api_key_here
python launcher.py
```

**Method B - Permanent (Windows 10):**
1. Open **System Properties** → **Advanced** → **Environment Variables**
2. Click "New" (under User variables)
3. Variable name: `GOOGLE_API_KEY`
4. Variable value: `your_api_key_here`
5. Click OK and restart Command Prompt

**Method C - In Python (Testing):**
```python
import os
os.environ['GOOGLE_API_KEY'] = 'your_api_key_here'

# Then run JARVIS
exec(open('jarvis_gemini.py').read())
```

---

#### **Option 2: OpenAI GPT-4o (Most Capable)**

💰 **PAID** (Requires subscription/credits)
🔥 Most advanced AI model
⚡ Better for complex tasks

1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Navigate to [API Keys](https://platform.openai.com/api-keys)
4. Click "Create new secret key"
5. Copy the key (save securely!)

**Set Environment Variable (Windows):**

**Method A - Temporary:**
```cmd
set OPENAI_API_KEY=your_api_key_here
python launcher.py
```

**Method B - Permanent:**
Same as above, but use `OPENAI_API_KEY` as variable name

**Method C - In Python:**
```python
import os
os.environ['OPENAI_API_KEY'] = 'your_api_key_here'

# Then run JARVIS
exec(open('jarvis.py').read())
```

---

## ▶️ Step 3: Launch JARVIS

### Method 1: Using Launcher (Recommended)

```cmd
python launcher.py
```

This will give you an interactive menu to:
- Check system requirements
- Choose between Gemini or OpenAI backend
- Select Voice or Text mode

### Method 2: Direct Launch

**Using Gemini:**
```cmd
python jarvis_gemini.py
```

**Using OpenAI:**
```cmd
python jarvis.py
```

---

## 🎤 Voice Commands Examples

Once JARVIS is running, try these commands:

### Opening Applications
```
"Open Chrome"
"Launch WhatsApp"
"Start Spotify"
"Open Visual Studio Code"
```

### Web Navigation
```
"Open Google"
"Visit YouTube"
"Search for Python tutorials"
"Go to GitHub"
```

### System Control
```
"Set volume to 50 percent"
"Mute audio"
"Unmute"
"Set brightness to 80"
"Lock the screen"
```

### Media Control
```
"Play music"
"Pause"
"Next track"
"Previous song"
```

### General Q&A
```
"What's the weather?"
"Tell me a joke"
"What time is it?"
"Explain Python"
```

---

## 📋 Supported Applications

| Category | Applications |
|----------|--------------|
| **Browsers** | Chrome, Firefox, Edge |
| **Communication** | WhatsApp, Discord, Telegram, Slack |
| **Productivity** | Notepad, Word, Excel, PowerPoint |
| **Development** | VSCode, Visual Studio, Terminal, PowerShell |
| **Media** | Spotify |
| **System** | Calculator |

---

## 🔧 Configuration

Edit `jarvis_gemini.py` or `jarvis.py` to customize:

```python
class Config:
    GEMINI_MODEL = "gemini-2.5-flash"  # AI model
    SPEECH_TIMEOUT = 10                 # Microphone listen timeout
    VOICE_RATE = 150                    # TTS speech speed
    VOICE_VOLUME = 0.9                  # TTS volume level
    DEBUG_MODE = True                   # Show debug messages
```

---

## ❌ Troubleshooting

### "ModuleNotFoundError: No module named 'google'"
**Solution:**
```cmd
pip install google-generativeai
```

### "OPENAI_API_KEY not set"
**Solution:**
```cmd
set OPENAI_API_KEY=your_key_here
python launcher.py
```

### "Microphone not working"
1. Check Windows Settings → Privacy & Security → Microphone
2. Grant microphone permission to Python
3. Test microphone in Sound settings

### "Speech recognition timeout"
- Speak louder and clearer
- Move closer to microphone
- Reduce background noise
- Increase `SPEECH_TIMEOUT` in config

### "Application won't open"
- Verify app is installed on your system
- Use exact application name
- Check application is in Windows PATH
- For portable apps, provide full path

### "Audio not playing"
- Check Windows volume is not muted
- Verify speaker is connected and working
- Test speakers with other apps
- Check TTS engine in Device Manager

---

## 🚀 Advanced Usage

### Running in Text Mode (No Microphone)

```cmd
python launcher.py
```
Then select option 2 (Text Command Mode)

Or directly:
```python
import jarvis_gemini
jarvis = jarvis_gemini.JARVIS()
jarvis.run("text")
```

### Custom System Prompt

Edit the `system_prompt` in the Brain class:

```python
self.system_prompt = """You are JARVIS, a witty AI assistant...
[Customize behavior here]
"""
```

### Extending with More Applications

In `OSControl` class, add to `app_mapping`:

```python
app_mapping = {
    "your_app": "your_app.exe",
    # Add more apps...
}
```

---

## 📊 System Requirements

| Component | Requirement |
|-----------|-------------|
| **OS** | Windows 10/11 |
| **Python** | 3.8 or higher |
| **RAM** | 2GB minimum (4GB recommended) |
| **Storage** | ~500MB for dependencies |
| **Internet** | Required for API calls |
| **Microphone** | Optional (for voice mode) |

---

## 📝 Features

✅ **Speech-to-Text (STT)** - Using Google Speech Recognition
✅ **Text-to-Speech (TTS)** - Using pyttsx3 (British male voice)
✅ **AI Backend** - Google Gemini 2.5 Flash or OpenAI GPT-4o
✅ **Application Launcher** - Open/close 15+ applications
✅ **Web Navigation** - Open websites and perform Google searches
✅ **System Control** - Volume, brightness, lock, sleep
✅ **Media Control** - Play, pause, skip tracks
✅ **Conversation Memory** - Context-aware responses
✅ **Error Handling** - Graceful fallbacks and logging
✅ **IDLE Compatible** - No GUI frameworks, pure CLI

---

## 🎯 Use Cases

1. **Hands-Free Computing**
   - "Open my project files"
   - "Search Stack Overflow"

2. **Smart Home Control**
   - "Lower the brightness"
   - "Mute the audio"

3. **Productivity**
   - "Open Word and create a document"
   - "Launch my IDE"

4. **Entertainment**
   - "Play my playlist"
   - "Skip to next song"

5. **Quick Information**
   - "What's the weather?"
   - "Tell me a joke"

---

## 📄 License

This project is open source. Use and modify freely!

---

## 🤝 Contributing

Found a bug? Want to add features?
1. Fork the repository
2. Make your changes
3. Submit a pull request

---

## 📞 Support

- **GitHub Issues:** [Report bugs](https://github.com/ruannchriz10/personal-ai-assistant/issues)
- **Documentation:** See README.md
- **API Docs:** 
  - [Gemini Docs](https://ai.google.dev/docs)
  - [OpenAI Docs](https://platform.openai.com/docs)

---

## ✨ Tips for Best Results

1. **Use clear speech** - Speak naturally and clearly
2. **Reduce background noise** - Quiet environment works best
3. **Allow microphone access** - Grant Python permissions in Windows
4. **Keep API quota** - Monitor usage to avoid overages
5. **Update regularly** - Keep dependencies updated

```cmd
pip install --upgrade google-generativeai openai SpeechRecognition
```

---

## 🎉 You're All Set!

Run `python launcher.py` and start using JARVIS today!

Enjoy your personal AI assistant! 🤖

