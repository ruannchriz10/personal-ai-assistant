#!/usr/bin/env python3
"""
================================================================================
JARVIS - Multi-Backend AI Assistant Launcher
================================================================================
Unified interface to launch JARVIS with either OpenAI GPT-4o or Google Gemini 2.5 Flash
"""

import os
import sys
import subprocess
from pathlib import Path

def print_banner():
    """Display JARVIS banner"""
    banner = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                                                                          ║
    ║                   JARVIS - Personal AI Assistant v1.0                    ║
    ║                                                                          ║
    ║              Windows 10 | Python IDLE | Multi-Backend Support           ║
    ║                                                                          ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    """
    print(banner)

def check_dependencies():
    """Check if all required packages are installed"""
    required_packages = {
        'speech_recognition': 'SpeechRecognition',
        'pyttsx3': 'pyttsx3',
        'openai': 'openai',
        'genai': 'google-generativeai'
    }
    
    missing = []
    for module, package in required_packages.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    if missing:
        print("\n[ERROR] Missing required packages:")
        for pkg in missing:
            print(f"  - {pkg}")
        print("\n[INFO] Install using:")
        print(f"  pip install {' '.join(missing)}")
        return False
    
    print("[SUCCESS] All dependencies found!")
    return True

def check_api_keys():
    """Check for required API keys"""
    print("\n[INFO] Checking API Keys...")
    
    openai_key = os.getenv("OPENAI_API_KEY", "")
    gemini_key = os.getenv("GOOGLE_API_KEY", "")
    
    if openai_key:
        print("  ✓ OpenAI API key detected")
    else:
        print("  ✗ OpenAI API key NOT found")
    
    if gemini_key:
        print("  ✓ Google Gemini API key detected")
    else:
        print("  ✗ Google Gemini API key NOT found")
    
    if not (openai_key or gemini_key):
        print("\n[WARNING] No API keys configured!")
        print("\nSet API keys using (Windows CMD):")
        print("  set OPENAI_API_KEY=your-openai-key")
        print("  set GOOGLE_API_KEY=your-gemini-key")
        print("\nOr in Python:")
        print("  import os")
        print("  os.environ['OPENAI_API_KEY'] = 'your-key-here'")
        print("  os.environ['GOOGLE_API_KEY'] = 'your-key-here'")
        return False
    
    return True

def select_backend():
    """Allow user to select AI backend"""
    print("\n" + "=" * 80)
    print("SELECT AI BACKEND:")
    print("=" * 80)
    print("\n1. Google Gemini 2.5 Flash (Recommended - Free with generous limits)")
    print("2. OpenAI GPT-4o (Most capable - Requires subscription)")
    print("3. Exit\n")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    return choice

def select_mode():
    """Allow user to select input mode"""
    print("\n" + "=" * 80)
    print("SELECT INPUT MODE:")
    print("=" * 80)
    print("\n1. Voice Command Mode (Requires microphone)")
    print("2. Text Command Mode (Keyboard input - for testing)")
    print("3. Back to menu\n")
    
    choice = input("Enter choice (1, 2, or 3): ").strip()
    
    return choice

def run_jarvis(backend: str, mode: str):
    """Run JARVIS with specified backend and mode"""
    
    mode_map = {
        "1": "voice",
        "2": "text",
        "voice": "voice",
        "text": "text"
    }
    
    actual_mode = mode_map.get(mode, "voice")
    
    # Set environment variable for JARVIS to know which mode to use
    os.environ['JARVIS_MODE'] = actual_mode
    
    try:
        if backend == "1" or backend.lower() == "gemini":
            print("\n[INFO] Launching JARVIS with Google Gemini 2.5 Flash...")
            exec(open('jarvis_gemini.py').read())
        
        elif backend == "2" or backend.lower() == "openai":
            print("\n[INFO] Launching JARVIS with OpenAI GPT-4o...")
            exec(open('jarvis.py').read())
        
        else:
            print("[ERROR] Invalid backend selection")
            return False
    
    except FileNotFoundError as e:
        print(f"[ERROR] Could not find JARVIS script: {e}")
        return False
    except Exception as e:
        print(f"[ERROR] Error running JARVIS: {e}")
        return False
    
    return True

def show_help():
    """Show help information"""
    help_text = """
    ╔══════════════════════════════════════════════════════════════════════════╗
    ║                         JARVIS HELP DOCUMENTATION                        ║
    ╚══════════════════════════════════════════════════════════════════════════╝
    
    GETTING STARTED:
    ================
    
    1. Install Dependencies:
       pip install -r requirements.txt
    
    2. Get API Keys:
       
       FOR GOOGLE GEMINI (Free, Recommended):
       - Visit: https://ai.google.dev/
       - Click "Get API Key" → "Create API key in new project"
       - Copy your key and set environment variable:
         set GOOGLE_API_KEY=your_key_here
       
       FOR OPENAI GPT-4o (Paid):
       - Visit: https://platform.openai.com/api-keys
       - Create new secret key
       - Set environment variable:
         set OPENAI_API_KEY=your_key_here
    
    3. Run JARVIS:
       python launcher.py
    
    
    VOICE COMMAND EXAMPLES:
    =======================
    
    • Open Applications:
      "JARVIS, open Chrome"
      "JARVIS, open WhatsApp"
      "JARVIS, launch Spotify"
    
    • Web Navigation:
      "JARVIS, open Google"
      "JARVIS, visit YouTube"
      "JARVIS, search for Python tutorials"
    
    • System Control:
      "JARVIS, set volume to 50 percent"
      "JARVIS, mute audio"
      "JARVIS, set brightness to 80"
      "JARVIS, lock the screen"
    
    • Media Control:
      "JARVIS, play the music"
      "JARVIS, pause"
      "JARVIS, next track"
      "JARVIS, previous song"
    
    • Information:
      "JARVIS, what time is it"
      "JARVIS, tell me a joke"
      "JARVIS, weather today"
    
    
    SUPPORTED APPLICATIONS:
    =======================
    
    • Browsers: Chrome, Firefox, Edge
    • Communication: WhatsApp, Discord, Telegram, Slack
    • Productivity: Notepad, Word, Excel, PowerPoint, VSCode
    • Media: Spotify
    • System: Calculator, Terminal, PowerShell
    
    
    SYSTEM REQUIREMENTS:
    ====================
    
    • Windows 10 (or later)
    • Python 3.8+
    • Microphone (for voice mode)
    • Active internet connection (for API calls)
    • Speaker/Headphones (for audio responses)
    
    
    TROUBLESHOOTING:
    ================
    
    • Microphone not working:
      - Check Windows microphone permissions
      - Test microphone in Settings > Privacy & Security
      - Adjust VOICE_TIMEOUT in jarvis_gemini.py if speech detection is slow
    
    • API key errors:
      - Verify API key is correctly set
      - Check you have active subscription (OpenAI) or quota (Gemini)
      - Test key in browser first
    
    • Application won't open:
      - Ensure application is installed and in system PATH
      - Use exact application name
      - Check Windows Task Manager for running processes
    
    • Audio not playing:
      - Check Windows speaker settings
      - Verify volume is not muted
      - Test speakers with other applications
    
    
    MORE HELP:
    ==========
    
    • GitHub: https://github.com/ruannchriz10/personal-ai-assistant
    • OpenAI Docs: https://platform.openai.com/docs
    • Gemini Docs: https://ai.google.dev/docs
    
    """
    print(help_text)

def main():
    """Main launcher loop"""
    
    print_banner()
    
    while True:
        print("\n" + "=" * 80)
        print("MAIN MENU:")
        print("=" * 80)
        print("\n1. Check System Requirements")
        print("2. Run JARVIS")
        print("3. Help & Documentation")
        print("4. Exit\n")
        
        choice = input("Enter choice (1, 2, 3, or 4): ").strip()
        
        if choice == "1":
            print("\n[INFO] Checking system requirements...\n")
            deps_ok = check_dependencies()
            api_ok = check_api_keys()
            
            if deps_ok and api_ok:
                print("\n[SUCCESS] All systems ready for launch!")
            else:
                print("\n[WARNING] Some issues detected. See above for details.")
        
        elif choice == "2":
            if not check_dependencies():
                print("\n[ERROR] Please install dependencies first (option 1)")
                continue
            
            backend = select_backend()
            
            if backend == "3":
                continue
            
            if backend not in ["1", "2"]:
                print("[ERROR] Invalid backend selection")
                continue
            
            mode = select_mode()
            
            if mode == "3":
                continue
            
            if mode not in ["1", "2"]:
                print("[ERROR] Invalid mode selection")
                continue
            
            print("\n" + "=" * 80)
            run_jarvis(backend, mode)
            print("=" * 80)
        
        elif choice == "3":
            show_help()
        
        elif choice == "4":
            print("\n[INFO] Exiting JARVIS Launcher. Goodbye!\n")
            break
        
        else:
            print("[ERROR] Invalid choice. Please try again.")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n[INFO] Launcher terminated by user. Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Fatal error: {e}")
        sys.exit(1)