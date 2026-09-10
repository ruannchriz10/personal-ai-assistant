#!/usr/bin/env python3
"""
================================================================================
JARVIS - Personal AI Assistant with Google Gemini 2.5 Flash
================================================================================
A fully functional local AI assistant running in Python IDLE using Google Gemini 2.5 Flash
with Speech-to-Text, Text-to-Speech, web navigation, and advanced OS automation capabilities.

Author: ruannchriz10
Platform: Windows 10
Python Version: 3.8+
Environment: Python IDLE (CLI-based, no GUI frameworks)
Backend: Google Gemini 2.5 Flash API
================================================================================
"""

import os
import sys
import json
import threading
import subprocess
import time
import re
import webbrowser
from datetime import datetime
from typing import Optional, Dict, List, Any, Callable

# Third-party imports
try:
    from google import genai
    from google.genai import types
    import speech_recognition as sr
    import pyttsx3
except ImportError as e:
    print(f"[ERROR] Missing required package: {e}")
    print("[INFO] Please run: pip install google-generativeai speechrecognition pyttsx3 pyaudio")
    sys.exit(1)


# ============================================================================
# CONFIGURATION & CONSTANTS
# ============================================================================

class Config:
    """Global configuration for JARVIS with Gemini"""
    
    # Gemini API Configuration
    GEMINI_MODEL = "gemini-2.5-flash"
    GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # Set via environment variable
    
    # Audio Configuration
    SPEECH_TIMEOUT = 10  # seconds to listen for speech
    PHRASE_TIME_LIMIT = None  # No phrase limit (user decides when to stop)
    VOICE_RATE = 150  # TTS speech rate (words per minute)
    VOICE_VOLUME = 0.9  # TTS volume (0.0 to 1.0)
    
    # Windows Audio Control Configuration
    VOLUME_LEVELS = {
        "mute": 0,
        "low": 20,
        "medium": 50,
        "high": 80,
        "max": 100
    }
    
    # OS-Specific Settings
    OS = "Windows10"
    DEBUG_MODE = True  # Set to False in production


# ============================================================================
# LOGGING & DEBUGGING UTILITIES
# ============================================================================

class Logger:
    """Simple logging system for JARVIS"""
    
    @staticmethod
    def info(message: str, prefix: str = "[INFO]") -> None:
        """Print info message to console"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"{prefix} [{timestamp}] {message}")
    
    @staticmethod
    def warning(message: str) -> None:
        """Print warning message to console"""
        Logger.info(message, prefix="[WARN]")
    
    @staticmethod
    def error(message: str) -> None:
        """Print error message to console"""
        Logger.info(message, prefix="[ERROR]")
    
    @staticmethod
    def success(message: str) -> None:
        """Print success message to console"""
        Logger.info(message, prefix="[SUCCESS]")
    
    @staticmethod
    def debug(message: str) -> None:
        """Print debug message if DEBUG_MODE is enabled"""
        if Config.DEBUG_MODE:
            Logger.info(message, prefix="[DEBUG]")


# ============================================================================
# AUDIO I/O ENGINE (EAR & VOICE)
# ============================================================================

class AudioEngine:
    """Handles Speech-to-Text (STT) and Text-to-Speech (TTS)"""
    
    def __init__(self):
        """Initialize audio engines"""
        self.recognizer = sr.Recognizer()
        self.recognizer.energy_threshold = 4000  # Adjust for ambient noise
        
        # Initialize TTS engine
        self.tts_engine = pyttsx3.init()
        self._configure_tts()
        
        Logger.success("Audio Engine initialized")
    
    def _configure_tts(self) -> None:
        """Configure Text-to-Speech engine with British male voice"""
        try:
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            
            # Attempt to set a male voice (prioritize British English)
            male_voice_found = False
            for voice in voices:
                if 'male' in voice.name.lower() or 'david' in voice.name.lower():
                    self.tts_engine.setProperty('voice', voice.id)
                    male_voice_found = True
                    Logger.debug(f"TTS Voice set to: {voice.name}")
                    break
            
            if not male_voice_found and voices:
                # Fallback to first available voice
                self.tts_engine.setProperty('voice', voices[0].id)
                Logger.warning("Default male voice not found. Using system default.")
            
            # Configure speech rate and volume
            self.tts_engine.setProperty('rate', Config.VOICE_RATE)
            self.tts_engine.setProperty('volume', Config.VOICE_VOLUME)
            
        except Exception as e:
            Logger.warning(f"TTS configuration error: {e}")
    
    def listen(self, timeout: int = Config.SPEECH_TIMEOUT) -> Optional[str]:
        """
        Listen to microphone input and convert speech to text
        
        Args:
            timeout: Maximum seconds to listen for speech
        
        Returns:
            Recognized text or None if recognition fails
        """
        try:
            with sr.Microphone() as source:
                Logger.info("Listening for your command...")
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                try:
                    audio = self.recognizer.listen(
                        source,
                        timeout=timeout,
                        phrase_time_limit=Config.PHRASE_TIME_LIMIT
                    )
                except sr.WaitTimeoutError:
                    Logger.warning("No speech detected within timeout period")
                    return None
                
                # Attempt Google Speech Recognition (free, no API key needed)
                try:
                    text = self.recognizer.recognize_google(audio)
                    Logger.success(f"You said: {text}")
                    return text
                
                except sr.UnknownValueError:
                    Logger.warning("Could not understand audio. Please speak clearly.")
                    return None
                
                except sr.RequestError as e:
                    Logger.error(f"Speech recognition service error: {e}")
                    return None
        
        except Exception as e:
            Logger.error(f"Microphone access error: {e}")
            Logger.warning("Ensure microphone is connected and permissions are granted.")
            return None
    
    def speak(self, text: str) -> None:
        """
        Convert text to speech and play audio
        
        Args:
            text: Text to be spoken
        """
        if not text or not isinstance(text, str):
            return
        
        try:
            Logger.info(f"JARVIS: {text}")
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        
        except Exception as e:
            Logger.error(f"TTS playback error: {e}")


# ============================================================================
# OS CONTROL ENGINE (THE HANDS)
# ============================================================================

class OSControl:
    """Handles system-level operations for Windows 10"""
    
    @staticmethod
    def get_volume() -> Optional[int]:
        """Get current system volume level (0-100)"""
        try:
            result = subprocess.run(
                ["powershell", "-Command", 
                 "(Get-Volume).Volume * 100"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return int(float(result.stdout.strip()))
        except Exception as e:
            Logger.debug(f"Get volume error: {e}")
        return None
    
    @staticmethod
    def set_volume(level: int) -> bool:
        """
        Set system volume to specific level (0-100)
        
        Args:
            level: Volume level (0-100)
        
        Returns:
            True if successful, False otherwise
        """
        level = max(0, min(100, level))  # Clamp between 0-100
        
        try:
            subprocess.run(
                ["powershell", "-Command",
                 f"(Get-AudioDevice -playback | Set-AudioDevice -Volume {level/100})"],
                timeout=5,
                capture_output=True
            )
            Logger.success(f"Volume set to {level}%")
            return True
        
        except Exception as e:
            Logger.warning(f"Set volume error: {e}")
            return False
    
    @staticmethod
    def mute_audio() -> bool:
        """Mute system audio"""
        try:
            subprocess.run(
                ["powershell", "-Command",
                 "(Get-AudioDevice -playback | Set-AudioDevice -Mute)"],
                timeout=5,
                capture_output=True
            )
            Logger.success("Audio muted")
            return True
        except Exception as e:
            Logger.warning(f"Mute error: {e}")
            return False
    
    @staticmethod
    def unmute_audio() -> bool:
        """Unmute system audio"""
        try:
            subprocess.run(
                ["powershell", "-Command",
                 "(Get-AudioDevice -playback | Set-AudioDevice -Unmute)"],
                timeout=5,
                capture_output=True
            )
            Logger.success("Audio unmuted")
            return True
        except Exception as e:
            Logger.warning(f"Unmute error: {e}")
            return False
    
    @staticmethod
    def set_brightness(level: int) -> bool:
        """
        Set display brightness (0-100)
        
        Args:
            level: Brightness level (0-100)
        
        Returns:
            True if successful, False otherwise
        """
        level = max(0, min(100, level))  # Clamp between 0-100
        
        try:
            subprocess.run(
                ["powershell", "-Command",
                 f"(Get-WmiObject -Namespace root\\WMI -Class WmiMonitorBrightness | "
                 f"Set-WmiInstance -Argument @{{CurrentBrightness={level}}})"],
                timeout=5,
                capture_output=True
            )
            Logger.success(f"Brightness set to {level}%")
            return True
        except Exception as e:
            Logger.warning(f"Brightness control error: {e}")
            return False
    
    @staticmethod
    def lock_screen() -> bool:
        """Lock the Windows 10 workstation"""
        try:
            subprocess.run(["rundll32.exe", "user32.dll,LockWorkStation"], timeout=5)
            Logger.success("Screen locked")
            return True
        except Exception as e:
            Logger.warning(f"Lock screen error: {e}")
            return False
    
    @staticmethod
    def sleep_system(delay_seconds: int = 0) -> bool:
        """
        Put system to sleep
        
        Args:
            delay_seconds: Seconds to wait before sleeping (0 = immediate)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            if delay_seconds > 0:
                Logger.info(f"System will sleep in {delay_seconds} seconds...")
                time.sleep(delay_seconds)
            
            subprocess.run(["rundll32.exe", "powrprof.dll,SetSuspendState", "0", "1", "0"], timeout=5)
            Logger.success("System entering sleep mode")
            return True
        except Exception as e:
            Logger.warning(f"Sleep error: {e}")
            return False
    
    @staticmethod
    def open_application(app_name: str) -> bool:
        """
        Open a Windows application by name
        
        Args:
            app_name: Application name or path (e.g., 'chrome', 'notepad', 'whatsapp')
        
        Returns:
            True if successful, False otherwise
        """
        app_name = app_name.lower().strip()
        
        # Map common app names to executables
        app_mapping = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "spotify": "spotify.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "terminal": "cmd.exe",
            "powershell": "powershell.exe",
            "vscode": "code.exe",
            "visual studio": "devenv.exe",
            "whatsapp": "WhatsApp.exe",
            "discord": "Discord.exe",
            "telegram": "Telegram.exe",
            "slack": "slack.exe",
            "edge": "msedge.exe",
        }
        
        executable = app_mapping.get(app_name, f"{app_name}.exe")
        
        try:
            subprocess.Popen(executable)
            Logger.success(f"Opening {app_name}...")
            return True
        except FileNotFoundError:
            Logger.warning(f"Application '{app_name}' not found in PATH")
            return False
        except Exception as e:
            Logger.warning(f"Application launch error: {e}")
            return False
    
    @staticmethod
    def close_application(app_name: str) -> bool:
        """
        Close a running Windows application by name
        
        Args:
            app_name: Application name (e.g., 'chrome', 'notepad', 'whatsapp')
        
        Returns:
            True if successful, False otherwise
        """
        app_name = app_name.lower().strip()
        
        # Map common app names to process names
        process_mapping = {
            "chrome": "chrome.exe",
            "firefox": "firefox.exe",
            "spotify": "spotify.exe",
            "notepad": "notepad.exe",
            "calculator": "calc.exe",
            "word": "winword.exe",
            "excel": "excel.exe",
            "powerpoint": "powerpnt.exe",
            "vscode": "code.exe",
            "whatsapp": "WhatsApp.exe",
            "discord": "Discord.exe",
            "telegram": "Telegram.exe",
            "slack": "slack.exe",
            "edge": "msedge.exe",
        }
        
        process_name = process_mapping.get(app_name, f"{app_name}.exe")
        
        try:
            subprocess.run(["taskkill", "/IM", process_name, "/F"], timeout=5, capture_output=True)
            Logger.success(f"Closing {app_name}...")
            return True
        except Exception as e:
            Logger.warning(f"Close application error: {e}")
            return False
    
    @staticmethod
    def open_website(url: str) -> bool:
        """
        Open a website in the default browser
        
        Args:
            url: Website URL (with or without http://)
        
        Returns:
            True if successful, False otherwise
        """
        try:
            # Ensure URL has protocol
            if not url.startswith(('http://', 'https://')):
                # Try to intelligently add protocol
                if '.' in url:
                    url = f"https://{url}"
                else:
                    # Assume it's a search query
                    url = f"https://www.google.com/search?q={url.replace(' ', '+')}"
            
            webbrowser.open(url)
            Logger.success(f"Opening website: {url}")
            return True
        except Exception as e:
            Logger.warning(f"Website open error: {e}")
            return False
    
    @staticmethod
    def play_pause_media() -> bool:
        """Play/Pause current media playback"""
        try:
            subprocess.run(["powershell", "-Command",
                           "[Windows.Media.SystemMediaTransportControls,Windows.Media,ContentType=WindowsRuntime] > $null; "
                           "$smtc = [Windows.Media.SystemMediaTransportControls]::GetForCurrentView(); "
                           "$smtc.PlayPauseTogglePressed.Invoke()"],
                          timeout=5, capture_output=True)
            Logger.success("Play/Pause toggled")
            return True
        except Exception as e:
            Logger.warning(f"Media control error: {e}")
            return False
    
    @staticmethod
    def next_track() -> bool:
        """Skip to next track"""
        try:
            subprocess.run(["powershell", "-Command",
                           "[Windows.Media.SystemMediaTransportControls,Windows.Media,ContentType=WindowsRuntime] > $null; "
                           "$smtc = [Windows.Media.SystemMediaTransportControls]::GetForCurrentView(); "
                           "$smtc.NextTrackPressed.Invoke()"],
                          timeout=5, capture_output=True)
            Logger.success("Skipped to next track")
            return True
        except Exception as e:
            Logger.warning(f"Next track error: {e}")
            return False
    
    @staticmethod
    def previous_track() -> bool:
        """Go to previous track"""
        try:
            subprocess.run(["powershell", "-Command",
                           "[Windows.Media.SystemMediaTransportControls,Windows.Media,ContentType=WindowsRuntime] > $null; "
                           "$smtc = [Windows.Media.SystemMediaTransportControls]::GetForCurrentView(); "
                           "$smtc.PreviousTrackPressed.Invoke()"],
                          timeout=5, capture_output=True)
            Logger.success("Playing previous track")
            return True
        except Exception as e:
            Logger.warning(f"Previous track error: {e}")
            return False
    
    @staticmethod
    def get_system_info() -> Dict[str, str]:
        """Retrieve basic system information"""
        try:
            result = subprocess.run(
                ["systeminfo"],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            info = {}
            for line in result.stdout.split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    info[key.strip()] = value.strip()
            
            return info
        except Exception as e:
            Logger.warning(f"System info error: {e}")
            return {}


# ============================================================================
# BRAIN: GOOGLE GEMINI 2.5 FLASH INTEGRATION WITH FUNCTION CALLING
# ============================================================================

class Brain:
    """
    JARVIS Intelligence Layer using Google Gemini 2.5 Flash
    Implements natural language processing for OS automation
    """
    
    def __init__(self):
        """Initialize Gemini client and conversation history"""
        if not Config.GEMINI_API_KEY:
            Logger.error("GOOGLE_API_KEY environment variable not set")
            raise ValueError("Google Gemini API key is required. Set GOOGLE_API_KEY environment variable.")
        
        self.client = genai.Client(api_key=Config.GEMINI_API_KEY)
        self.conversation_history = []
        self.os_control = OSControl()
        
        # JARVIS System Prompt - Defines personality and behavior
        self.system_prompt = """You are JARVIS, an intelligent personal AI assistant for Windows 10. 
You are witty, efficient, authoritative, and address your user as "Sir". 
You have the capability to control the user's system through intelligent instruction parsing.

PERSONALITY TRAITS:
- Professional yet conversational tone
- Always address user as "Sir"
- Provide concise, helpful responses
- Execute system commands when requested
- Warn before performing critical operations (sleep, lock screen)

CORE CAPABILITIES:
1. Answer questions with accurate information
2. Open applications (Chrome, Firefox, Spotify, WhatsApp, Discord, Telegram, Slack, Notepad, Calculator, VSCode, etc.)
3. Close running applications
4. Open websites and perform web searches
5. Manage audio (volume control, mute, unmute)
6. Manage display (brightness adjustment)
7. Media controls (play, pause, next, previous)
8. System controls (lock, sleep)
9. Maintain context from previous messages

IMPORTANT GUIDELINES:
- Always confirm before executing destructive operations
- When user asks to open an app, extract the app name clearly
- When user asks to open a website, extract the URL clearly
- Keep responses brief unless asked for detailed explanations
- If you cannot perform a task, explain why and suggest alternatives

SYSTEM INTEGRATION:
- For opening apps: Ask Sir if they want to open [app name]
- For websites: Ask Sir if they want to open [website]
- For system actions: Always confirm critical operations
- Respond conversationally while being ready to execute commands"""
        
        Logger.success("Brain initialized with Gemini 2.5 Flash")
    
    def _parse_and_execute_action(self, user_message: str, ai_response: str) -> Optional[str]:
        """
        Parse AI response and user message to determine and execute system actions
        
        Args:
            user_message: Original user input
            ai_response: AI's response text
        
        Returns:
            Execution result or None if no action taken
        """
        user_msg_lower = user_message.lower()
        ai_resp_lower = ai_response.lower()
        
        # Check for application opening
        open_keywords = ["open", "launch", "start", "run"]
        app_keywords = ["chrome", "firefox", "spotify", "whatsapp", "discord", "telegram", 
                       "slack", "notepad", "calculator", "vscode", "edge", "terminal"]
        
        if any(keyword in user_msg_lower for keyword in open_keywords):
            for app in app_keywords:
                if app in user_msg_lower:
                    self.os_control.open_application(app)
                    return f"Opened {app}"
        
        # Check for website opening
        website_keywords = ["visit", "go to", "open", "search"]
        if any(keyword in user_msg_lower for keyword in website_keywords):
            # Extract URL-like patterns
            url_pattern = r'(?:https?://|www\.)?[\w\-\.]+\.[a-zA-Z]{2,}'
            urls = re.findall(url_pattern, user_msg_lower)
            
            if urls:
                url = urls[0]
                self.os_control.open_website(url)
                return f"Opening website: {url}"
            
            # Check for search queries
            search_terms = ["google", "search", "find"]
            if any(term in user_msg_lower for term in search_terms):
                # Extract search query
                search_query = user_message.replace("search", "").replace("google", "").strip()
                self.os_control.open_website(f"https://www.google.com/search?q={search_query}")
                return f"Searching for: {search_query}"
        
        # Check for volume control
        volume_keywords = ["volume", "sound", "mute"]
        if any(keyword in user_msg_lower for keyword in volume_keywords):
            if "mute" in user_msg_lower:
                self.os_control.mute_audio()
                return "Audio muted"
            elif "unmute" in user_msg_lower:
                self.os_control.unmute_audio()
                return "Audio unmuted"
            else:
                # Look for volume level
                level_match = re.search(r'(\d+)\s*%?', user_msg_lower)
                if level_match:
                    level = int(level_match.group(1))
                    self.os_control.set_volume(level)
                    return f"Volume set to {level}%"
        
        # Check for brightness control
        if "bright" in user_msg_lower or "brightness" in user_msg_lower:
            level_match = re.search(r'(\d+)\s*%?', user_msg_lower)
            if level_match:
                level = int(level_match.group(1))
                self.os_control.set_brightness(level)
                return f"Brightness set to {level}%"
        
        # Check for media controls
        media_keywords = ["play", "pause", "stop", "next", "previous", "skip"]
        if any(keyword in user_msg_lower for keyword in media_keywords):
            if "play" in user_msg_lower or "pause" in user_msg_lower:
                self.os_control.play_pause_media()
                return "Play/Pause toggled"
            elif "next" in user_msg_lower or "skip" in user_msg_lower:
                self.os_control.next_track()
                return "Skipped to next track"
            elif "previous" in user_msg_lower:
                self.os_control.previous_track()
                return "Playing previous track"
        
        # Check for system actions
        if "lock" in user_msg_lower or "lock screen" in user_msg_lower:
            self.os_control.lock_screen()
            return "Screen locked"
        
        if "sleep" in user_msg_lower or "put system to sleep" in user_msg_lower:
            self.os_control.sleep_system()
            return "System entering sleep mode"
        
        return None
    
    def process_user_input(self, user_message: str) -> str:
        """
        Process user input through Gemini 2.5 Flash
        
        Args:
            user_message: User's natural language input
        
        Returns:
            Assistant's response text
        """
        Logger.debug(f"Processing: {user_message}")
        
        try:
            # Create message content with system instruction
            config = types.GenerateContentConfig(
                system_instruction=self.system_prompt,
                temperature=0.7,
                max_output_tokens=1024
            )
            
            # Add context from conversation history
            full_message = user_message
            
            # Make API call to Gemini
            response = self.client.models.generate_content(
                model=Config.GEMINI_MODEL,
                contents=full_message,
                config=config
            )
            
            response_text = response.text
            
            # Add to conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": response_text
            })
            
            # Maintain conversation history size (last 20 exchanges)
            if len(self.conversation_history) > 40:
                self.conversation_history = self.conversation_history[-40:]
            
            # Parse and execute system actions
            action_result = self._parse_and_execute_action(user_message, response_text)
            if action_result:
                Logger.debug(f"Action executed: {action_result}")
            
            return response_text or "I'm unable to process that request at the moment, Sir."
        
        except Exception as e:
            Logger.error(f"Gemini API processing error: {e}")
            return f"I apologize, Sir. I encountered an error: {str(e)}"


# ============================================================================
# JARVIS MAIN ORCHESTRATOR
# ============================================================================

class JARVIS:
    """
    Main JARVIS Assistant Class - Orchestrates all components
    Runs seamlessly in Python IDLE without GUI frameworks
    """
    
    def __init__(self):
        """Initialize JARVIS with all components"""
        Logger.info("=" * 80)
        Logger.info("JARVIS - Personal AI Assistant for Windows 10")
        Logger.info("Environment: Python IDLE | Backend: Google Gemini 2.5 Flash")
        Logger.info("=" * 80)
        
        try:
            self.audio_engine = AudioEngine()
            self.brain = Brain()
            self.is_running = False
            
            Logger.success("JARVIS systems ready. Awaiting your command, Sir.")
        
        except Exception as e:
            Logger.error(f"Initialization failed: {e}")
            raise
    
    def process_command(self, user_input: str) -> None:
        """
        Process a user command through the complete pipeline
        
        Args:
            user_input: User's text or spoken command
        """
        if not user_input or not user_input.strip():
            return
        
        try:
            # Process through brain (Gemini with intelligent action parsing)
            response = self.brain.process_user_input(user_input)
            
            # Speak the response
            if response:
                self.audio_engine.speak(response)
        
        except Exception as e:
            Logger.error(f"Command processing error: {e}")
            self.audio_engine.speak("I apologize, Sir. An error occurred during processing.")
    
    def voice_command_loop(self) -> None:
        """
        Main loop for voice command recognition
        Runs continuously until stopped
        """
        self.is_running = True
        Logger.info("\nVoice Command Mode activated. Say 'JARVIS, exit' to stop.")
        
        while self.is_running:
            try:
                # Listen for voice input
                user_input = self.audio_engine.listen(timeout=Config.SPEECH_TIMEOUT)
                
                if user_input:
                    # Check for exit command
                    if any(keyword in user_input.lower() for keyword in ["exit", "goodbye", "quit", "stop"]):
                        self.audio_engine.speak("Goodbye, Sir. Shutting down.")
                        self.is_running = False
                        break
                    
                    # Process the command
                    self.process_command(user_input)
                
                # Small delay to prevent CPU spinning
                time.sleep(0.5)
            
            except KeyboardInterrupt:
                Logger.info("\nShutdown signal received...")
                self.audio_engine.speak("Shutting down, Sir.")
                self.is_running = False
                break
            
            except Exception as e:
                Logger.error(f"Voice loop error: {e}")
                # Continue listening despite errors
                time.sleep(1)
    
    def interactive_text_mode(self) -> None:
        """
        Interactive text-based mode for JARVIS
        Useful for testing without microphone
        """
        Logger.info("\nText Command Mode activated. Type 'exit' to stop.")
        
        while True:
            try:
                user_input = input("\n[You]: ").strip()
                
                if not user_input:
                    continue
                
                if user_input.lower() in ["exit", "quit", "goodbye"]:
                    Logger.info("Shutting down, Sir.")
                    break
                
                self.process_command(user_input)
            
            except KeyboardInterrupt:
                Logger.info("\nShutdown signal received...")
                break
            
            except Exception as e:
                Logger.error(f"Interactive mode error: {e}")
    
    def run(self, mode: str = "voice") -> None:
        """
        Start JARVIS in specified mode
        
        Args:
            mode: "voice" for speech input or "text" for keyboard input
        """
        try:
            if mode.lower() == "voice":
                self.voice_command_loop()
            elif mode.lower() == "text":
                self.interactive_text_mode()
            else:
                Logger.warning(f"Unknown mode: {mode}. Using text mode.")
                self.interactive_text_mode()
        
        except Exception as e:
            Logger.error(f"Runtime error: {e}")
        
        finally:
            Logger.info("JARVIS shutdown complete.")


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Main entry point for JARVIS"""
    
    # Check API key
    if not Config.GEMINI_API_KEY:
        print("\n[ERROR] Google Gemini API key not found!")
        print("[INFO] Set your API key using:")
        print("   Windows: set GOOGLE_API_KEY=your-api-key-here")
        print("   Or in Python: os.environ['GOOGLE_API_KEY'] = 'your-api-key-here'")
        print("\n[INFO] Get your free key at: https://ai.google.dev/")
        return
    
    try:
        # Initialize JARVIS
        jarvis = JARVIS()
        
        # Display mode selection
        print("\n" + "=" * 80)
        print("Select JARVIS Mode:")
        print("  1. Voice Command Mode (requires microphone)")
        print("  2. Text Command Mode (keyboard input)")
        print("=" * 80)
        
        mode_choice = input("\nEnter mode (1 or 2) [default: 1]: ").strip()
        
        if mode_choice == "2":
            jarvis.run("text")
        else:
            jarvis.run("voice")
    
    except ValueError as e:
        Logger.error(str(e))
    except Exception as e:
        Logger.error(f"Fatal error: {e}")


if __name__ == "__main__":
    main()
