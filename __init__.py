# Import Tools
import os
import sys
import configparser
import random
import speech_recognition as sr
import pyaudio
import pyttsx3

# Import Custom module
from JARVIS.modules.face_identification import FaceRecognition
from JARVIS.modules.weather import Weather
from JARVIS.modules.date import Date
from JARVIS.modules.time import Time
from JARVIS.modules.setup import Setup
from JARVIS.modules.wake_word import WakeWord, DefaultFileNotFound


class Jarvis:
    def _init__(self):
        pass

    def hot_word_detect(self, lang='en'):
        """
        Hot word (wake word / background listen) detection
        :param lang: str
            default 'en'
        :return: Bool, str
            status, command
        """
        try:
            status, command = WakeWord.Wake_word(self, lang=lang)
        except DefaultFileNotFound as e:
            print(
                "Unable to locate configuraton file './JARVIS/config/config.ini'. Creating NOW...")
            self.setup()
        except Exception as e:
            status = command = False
        return status, command

    def mic_input(self, lang='en'):
        """
        Fetch input from mic
        :param lang: str
            default 'en'
        :return: str/Bool
            user's voice input as text if true/ false if fail
        """
        config = configparser.ConfigParser()
        config.read('./JARVIS/config/config.ini')
        user_name = config['default']['user_name']

        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                greeting = random.choice(["Hello", "Hi"])
                msg = f'{greeting} {user_name} , How may I help you?'
                print(msg)
                self.text2speech(msg)
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source)
            try:
                command = r.recognize_google(audio, language=lang).lower()
                print(f'You said: {command} \n')
            except sr.UnknownValueError:
                print('....')
                command = self.mic_input()
            return command
        except Exception as e:
            print(e)
            return False

    def text2speech(self, text):
        """
        Convert any text to speech
        :param text: str
            text (String)
        :return: Bool
            True / False (Play sound if True otherwise write exception to log and return False)
        """
        try:
            engine = pyttsx3.init()
            voices = engine.getProperty("voices")
            engine.setProperty("voice", voices[1].id)
            engine.say(text)
            engine.runAndWait()
            return True
        except Exception as e:
            mytext = "Sorry I couldn't understand, or not implemented to handle this input"
            print(mytext)
            print(e)
            return False

    def tell_me_date(self):
        """
        Just return date as string
        :return: str/Bool
            date if success, False if fail
        """
        return Date.date()

    def tell_me_time(self):
        """
        This function will return time
        :return: str/Bool
            Time if success, False if fail
        """
        return Time.time()

    def face_recognition(self):
        pass

    def weather_info(self, city='Vadodara'):
        """
        Return weather
        :param city: str
            Any city of this world
        :return: str/bool
            weather info as string if True, or False
        """
        try:
            obj = Weather()
            res = obj.weather_app(city)
        except Exception as e:
            print(e)
            res = False
        return res

    def shutdown(self):
        """
        Shutdown the Jarvis API, exit from program
        :return: None/bool
            if no error then exit from program, False if Fail
        """
        try:
            sys.exit()
        except Exception as e:
            print(e)
            return False

    def setup(self):
        """
        Method to define configuration related to assistant
        :return: Bool
            True if setup done
            False if setup cancel or interrupt
        """
        obj_setup = Setup()
        response = obj_setup.setup_assistant()
        del obj_setup
        return response


if __name__ == '__main__':
    obj = Jarvis()
