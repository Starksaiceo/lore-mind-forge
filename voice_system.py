import os
import json
import time
from typing import Dict, Any, Optional
import requests
from gtts import gTTS
import pygame
import io
import speech_recognition as sr
from threading import Thread
import queue

class VoiceSystem:
    def __init__(self):
        self.tts_enabled = False
        self.voice_type = "professional"
        self.agent_name = "AI CEO"
        self.personality = "professional"

        # Initialize pygame mixer for audio playback
        try:
            pygame.mixer.init()
            self.audio_available = True
        except:
            self.audio_available = False

        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = None
        try:
            self.microphone = sr.Microphone()
            self.stt_available = True
        except:
            self.stt_available = False

    def speak_text(self, text: str, language: str = 'en') -> bool:
        """Convert text to speech and play it"""
        if not self.tts_enabled or not self.audio_available:
            return False

        try:
            # Use gTTS for free text-to-speech
            tts = gTTS(text=text, lang=language, slow=False)

            # Save to memory buffer
            audio_buffer = io.BytesIO()
            tts.write_to_fp(audio_buffer)
            audio_buffer.seek(0)

            # Play audio using pygame
            pygame.mixer.music.load(audio_buffer)
            pygame.mixer.music.play()

            # Wait for audio to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)

            return True
        except Exception as e:
            print(f"TTS Error: {e}")
            return False

    def listen_for_speech(self, timeout: int = 5) -> Optional[str]:
        """Convert speech to text"""
        if not self.stt_available or not self.microphone:
            return None

        try:
            with self.microphone as source:
                # Adjust for ambient noise
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                print("🎤 Listening...")

                # Listen for audio
                audio = self.recognizer.listen(source, timeout=timeout, phrase_time_limit=10)

                # Convert to text using Google Speech Recognition (free)
                text = self.recognizer.recognize_google(audio)
                print(f"🎤 Heard: {text}")
                return text

        except sr.WaitTimeoutError:
            print("🎤 Listening timeout")
            return None
        except sr.UnknownValueError:
            print("🎤 Could not understand audio")
            return None
        except sr.RequestError as e:
            print(f"🎤 Speech recognition error: {e}")
            return None

    def get_personality_prompt(self) -> str:
        """Get personality-based system prompt"""
        personalities = {
            "professional": "You are a professional AI business partner. Be intelligent, helpful, and slightly witty. Keep responses concise but thorough.",
            "funny": "You are a fun-loving AI business partner who loves to crack jokes and keep things light while still being incredibly helpful and smart.",
            "serious": "You are a serious, no-nonsense AI business partner focused purely on results and efficiency. Be direct and actionable.",
            "hustler": "You are a street-smart AI business partner with an entrepreneurial spirit. Talk like you've been in the game and know how to make money.",
            "coach": "You are a motivational AI business coach. Be encouraging, supportive, and help push your partner to achieve their goals."
        }

        base_prompt = personalities.get(self.personality, personalities["professional"])
        return f"{base_prompt} Your name is {self.agent_name}. Always introduce yourself by name when appropriate."

class PersonalityManager:
    def __init__(self, db_connection):
        self.db = db_connection

    def load_user_preferences(self, user_id: int) -> Dict[str, Any]:
        """Load user's voice and personality preferences"""
        try:
            from sqlalchemy import text
            cursor = self.db.execute(
                text("SELECT voice_enabled, agent_name, personality, voice_type FROM user_preferences WHERE user_id = ?"),
                (user_id,)
            )
            result = cursor.fetchone()

            if result:
                return {
                    "voice_enabled": bool(result[0]),
                    "agent_name": result[1] or "AI CEO",
                    "personality": result[2] or "professional",
                    "voice_type": result[3] or "professional"
                }
            else:
                # Create default preferences
                self.save_user_preferences(user_id, {
                    "voice_enabled": False,
                    "agent_name": "AI CEO",
                    "personality": "professional",
                    "voice_type": "professional"
                })
                return {
                    "voice_enabled": False,
                    "agent_name": "AI CEO",
                    "personality": "professional",
                    "voice_type": "professional"
                }
        except Exception as e:
            print(f"Error loading preferences: {e}")
            return {
                "voice_enabled": False,
                "agent_name": "AI CEO",
                "personality": "professional",
                "voice_type": "professional"
            }

    def save_user_preferences(self, user_id: int, preferences: Dict[str, Any]) -> bool:
        """Save user's voice and personality preferences"""
        try:
            from sqlalchemy import text
            self.db.execute(text('''
                INSERT OR REPLACE INTO user_preferences 
                (user_id, voice_enabled, agent_name, personality, voice_type, updated_at)
                VALUES (?, ?, ?, ?, ?, datetime('now'))
            '''), (
                user_id,
                int(preferences.get("voice_enabled", False)),
                preferences.get("agent_name", "AI CEO"),
                preferences.get("personality", "professional"),
                preferences.get("voice_type", "professional")
            ))
            self.db.commit()
            return True
        except Exception as e:
            print(f"Error saving preferences: {e}")
            return False

def get_personality_voice_settings(personality):
    """Get voice settings for personality"""
    settings = {
        'professional': {"pitch": 1.0, "rate": 0.9, "volume": 0.8},
        'funny': {"pitch": 1.4, "rate": 1.3, "volume": 0.9},
        'serious': {"pitch": 0.8, "rate": 0.9, "volume": 0.95},
        'motivational': {"pitch": 1.1, "rate": 1.0, "volume": 1.0},
        'luxury': {"pitch": 0.9, "rate": 0.95, "volume": 1.0},
        'enthusiastic': {"pitch": 1.3, "rate": 1.2, "volume": 1.0},
        'calm': {"pitch": 0.9, "rate": 0.85, "volume": 0.8},
        'analytical': {"pitch": 1.0, "rate": 0.95, "volume": 0.9},
        'visionary': {"pitch": 1.1, "rate": 1.0, "volume": 0.95},
        'results_driven': {"pitch": 1.0, "rate": 1.1, "volume": 1.0},
        'innovative': {"pitch": 1.2, "rate": 1.05, "volume": 0.95}
    }
    return settings.get(personality, settings['professional'])

def generate_personality_response(command, personality, agent_name):
    """Generate personality-matched response to voice commands"""
    command_lower = command.lower()

    # Personality-specific greetings and styles
    personality_styles = {
        'professional': {
            'greeting': f"This is {agent_name}.",
            'style': 'formal and efficient',
            'responses': {
                'profit': f"Your current revenue metrics show strong performance.",
                'create': f"I'll initiate the creation process for you.",
                'status': f"Here's your comprehensive business status.",
                'default': f"I'm ready to assist with your business objectives."
            }
        },
        'funny': {
            'greeting': f"Hey there! {agent_name} reporting for comedy duty! 😄",
            'style': 'playful and humorous',
            'responses': {
                'profit': f"Ka-ching! Your money machine is working! Don't spend it all on pizza. 🍕",
                'create': f"Time to birth some digital babies! This is gonna be fun! 🚀",
                'status': f"Let me check your empire... *shuffles papers dramatically*",
                'default': f"What's the plan, boss? I'm ready to make some magic happen! ✨"
            }
        },
        'motivational': {
            'greeting': f"{agent_name} here! Ready to CRUSH your goals today! 💪",
            'style': 'energetic and inspiring',
            'responses': {
                'profit': f"BOOM! Your profits are climbing! Keep that momentum going, champion!",
                'create': f"Let's CREATE something that changes the game! You've got this!",
                'status': f"Look at you conquering the business world! Here's your victory report!",
                'default': f"Whatever challenge you're facing, we'll DOMINATE it together!"
            }
        },
        'luxury': {
            'greeting': f"Good day. This is {agent_name}, your premium business advisor. 💎",
            'style': 'sophisticated and refined',
            'responses': {
                'profit': f"Your portfolio performance is most impressive. Quite sophisticated returns.",
                'create': f"We shall craft something truly exceptional. Only the finest quality.",
                'status': f"Allow me to present your distinguished business metrics.",
                'default': f"How may I provide my premium expertise today?"
            }
        },
        'analytical': {
            'greeting': f"{agent_name} online. Data analysis mode activated. 📊",
            'style': 'data-driven and precise',
            'responses': {
                'profit': f"Revenue analysis complete. ROI trending positive at optimal parameters.",
                'create': f"Initiating creation sequence with maximum efficiency protocols.",
                'status': f"Comprehensive metrics analysis: All systems operational.",
                'default': f"Processing request. Calculating optimal solution pathways."
            }
        }
    }

    # Get style for current personality (fallback to professional)
    current_style = personality_styles.get(personality, personality_styles['professional'])

    # Determine response based on command content
    if any(word in command_lower for word in ['profit', 'money', 'revenue', 'income']):
        response = current_style['responses']['profit']
    elif any(word in command_lower for word in ['create', 'generate', 'make', 'build']):
        response = current_style['responses']['create']
    elif any(word in command_lower for word in ['status', 'report', 'dashboard', 'metrics']):
        response = current_style['responses']['status']
    else:
        response = current_style['responses']['default']

    return response

# Global voice system instance
voice_system = VoiceSystem()