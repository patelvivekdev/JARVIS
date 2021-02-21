# Import Tools
import speech_recognition as sr
import os
import pyttsx3
import pyaudio
import psutil
import wikipedia

# Import Custom module
try:
    import modules.face_identification
except Exception as e:
    import jarvis.modules.face_identification


class JarvisAssistant:
    def _init__(self):
        pass
