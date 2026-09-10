# JARVIS - Quick Start Guide

## 🚀 30-Second Setup

### Step 1: Install (1 minute)
```bash
pip install -r requirements.txt
```

### Step 2: Get API Key (2 minutes)

**Gemini (Free - Recommended):**
```bash
# Visit: https://ai.google.dev/
# Get your key and run:
set GOOGLE_API_KEY=your_key_here
```

**OpenAI (Paid):**
```bash
# Visit: https://platform.openai.com/api-keys
# Get your key and run:
set OPENAI_API_KEY=your_key_here
```

### Step 3: Run JARVIS (30 seconds)
```bash
python launcher.py
```

---

## 🎤 Voice Commands - Try These First

```
"Open Chrome"
"Search for Python tutorials"
"Set volume to 50"
"Play music"
"Next track"
"Tell me a joke"
"Lock the screen"
```

---

## 📝 Text Mode (No Microphone)

```bash
python launcher.py
```
Then select option 2 (Text Command Mode)

---

## ❌ Common Issues

### "Module not found"
```bash
pip install -r requirements.txt
```

### "API key error"
- Make sure you set the environment variable
- Verify key in browser first
- Check you have active subscription (OpenAI) or quota (Gemini)

### "Microphone not working"
- Check Windows Settings → Privacy → Microphone
- Grant permission to Python
- Test mic in Sound settings

### "PyAudio install fails"
```bash
pip install pipwin
pipwin install PyAudio
```

---

## 📚 Full Documentation

- **Setup Guide:** `SETUP_GUIDE.md`
- **Features & Architecture:** `README.md`
- **Source Code:** `jarvis_gemini.py` or `jarvis.py`

---

## 🎯 What JARVIS Can Do

✅ Answer questions
✅ Open applications (Chrome, WhatsApp, Spotify, etc.)
✅ Navigate websites
✅ Control volume and brightness
✅ Play/pause/skip music
✅ Lock screen and sleep system
✅ Understand context from conversation
✅ Remember previous exchanges

---

## 💡 Pro Tips

1. **Use Gemini first** - It's free and great for learning
2. **Speak clearly** - Say commands naturally
3. **Quiet environment** - Less background noise = better recognition
4. **Use text mode to test** - Before using voice mode
5. **Check console output** - Debug messages help troubleshoot

---

## 🆘 Need Help?

Check these resources:
- **GitHub Issues:** https://github.com/ruannchriz10/personal-ai-assistant/issues
- **Gemini Docs:** https://ai.google.dev/docs
- **OpenAI Docs:** https://platform.openai.com/docs

---

**Enjoy JARVIS! 🤖**
