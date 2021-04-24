# Import Tools
import os
import sys
import configparser
import datetime
import random
import speech_recognition as sr
import pyaudio
import pyttsx3
import psutil
import pyautogui

# Import Custom module
from JARVIS.modules.face_identification import FaceIdentificaion
from JARVIS.modules.weather import Weather
from JARVIS.modules.date import Date
from JARVIS.modules.time import Time
from JARVIS.modules.setup import Setup
from JARVIS.modules.wake_word import WakeWord, DefaultFileNotFound
from JARVIS.modules.wikipedia import Wikipedia
from JARVIS.modules.open_app import OpenApp
from JARVIS.modules.website_open import WebsiteOpen
from JARVIS.modules.face_identification.face_detection import user


class Jarvis:
    def _init__(self):
        pass

    def hot_word_detect(self, lang='en'):
        """
        Hot word (wake word / background listen) detection.

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

    def mic_input(self, lang='en-in'):
        """
        Fetch input from mic.

        :param lang: str
            default 'en-in'

        :return: str/Bool
            user's voice input as text if true/ false if fail
        """
        try:
            r = sr.Recognizer()
            with sr.Microphone() as source:
                print('listening.....')
                r.pause_threshold = 1
                r.adjust_for_ambient_noise(source, duration=1.5)
                audio = r.listen(source)
            try:
                print('Recognizing.....')
                command = r.recognize_google(audio, language=lang).lower()
                print(f'user said: {command} \n')
            except sr.UnknownValueError:
                print('....')
                command = self.mic_input()
            return command
        except Exception as e:
            print(e)
            return False

    def text2speech(self, text):
        """
        Convert any text to speech.

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

    def cpu(self):
        """
        Give current CPU and Buttery percent.

        :return: str/bool
        """
        try:
            usage = str(psutil.cpu_percent())
            print(f"CPU is at {usage}")
            self.text2speech("CPU is at " + usage)
            battery = psutil.sensors_battery()
            print("Battery is at", battery.percent)
            self.text2speech("Battery is at")
            self.text2speech(battery.percent)
        except Exception as e:
            print(e)
            return False

    def greeting(self):
        """
        Authenticate user through face identification. 
        """
        config = configparser.ConfigParser()
        config.read(r'./JARVIS/config/config.ini')
        user_name = config['default']['user_name']

        username = self.detect_person()

        if user_name == username:
            flag = False
            hour = datetime.datetime.now().hour
            if hour >= 6 and hour < 12:
                print(f"Good Morning! {user_name}")
                self.text2speech(f"Good Morning!{user_name}")
                flag = True
            elif hour >= 12 and hour < 18:
                print(f"Good Afternoon! {user_name}")
                self.text2speech(f"Good Afternoon!{user_name}")
                flag = True
            elif hour >= 18 and hour < 24:
                print(f"Good Evening! {user_name}")
                self.text2speech(f"Good Evening!{user_name}")
                flag = True
            else:
                print("it's time to bad sir ! Good night")
                self.text2speech("it's time to bad sir ! Good night")
                flag = False
            if flag:
                print("checking functionality")
                self.text2speech("checking functionality")
                self.cpu()
                print("How may i help you today?")
                self.text2speech("How may i help you today?")
        else:
            print('user unauthenticated')
            self.text2speech('user unauthenticated')
            sys.exit()

    def tell_me_date(self):
        """
        Just return date as string.

        :return: str/Bool
            date if success, False if fail
        """
        return Date.date()

    def tell_me_time(self):
        """
        This function will return time.

        :return: str/Bool
            Time if success, False if fail
        """
        return Time.time()

    def data_create(self, dataset_path=r'JARVIS\modules\face_identification\data',
                    class_name='demo',
                    no_of_samples=5,
                    width=300,
                    height=300,
                    caffemodel_path=r'JARVIS\modules\face_identification\model\res10_300x300_ssd_iter_140000.caffemodel',
                    prototxt_path=r'JARVIS\modules\face_identification\model\deploy.prototxt'):
        """
        Info : Dataset Create by face detection with OpenCV SSD.

        :param dataset_path: str (example: 'path_of_dataset')
        :param class_name: str (example: 'name_of_user')
        :param no_of_samples: int (example: 5)
        :param width: int (example: 300)
        :param height: int (example: 300)
        :param caffemodel_path : str (example: 'path_to_caffe_model')
        :param prototxt: str (example:'path_to_prototxt')
        :return: None
        """

        admin_username = input("Enter Admin username :")
        admin_password = input("Enter Admin password :")

        try:
            status, username = user.user_authentication(
                user_name=admin_username,
                user_pass=admin_password)
        except Exception as e:
            print(e)

        if status:
            print(f" {username} Authenticated...")
            user_name = input("Enter name of the new user:")
            obj = FaceIdentificaion()
            obj.face_detetion(class_name=user_name)
        else:
            print('Username or password is not match! Please try again.')

    def detect_person(self, data_path=r'JARVIS\modules\face_identification\data',
                      img_height=224,
                      img_width=224,
                      model_path=r'JARVIS\modules\face_identification\model\model.h5',
                      caffemodel_path=r'JARVIS\modules\face_identification\model\res10_300x300_ssd_iter_140000.caffemodel',
                      prototxt_path=r'JARVIS\modules\face_identification\model\deploy.prototxt'):
        """
        Info : Face_Recognition class

        :param data_path : str (example: 'Path_to_Data')
        :param img_heigth: int (example: 224)
        :param img_width: int (example: 224)
        :parma model_path: str (example: 'Path_To_Tensorflow_model')
        :param caffemodel_path : str (example: 'path_to_caffe_model')
        :param prototxt: str (example:'path_to_prototxt')

        :return: final person name
        """
        obj = FaceIdentificaion()

        user_name = obj.face_recognition(
            data_path, img_height, img_width, model_path, caffemodel_path, prototxt_path)

        return user_name

    def weather_info(self, city='Vadodara'):
        """
        Return weather information about the city.

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

    def website_opener(self, domain):
        """
        This will open website according to domain
        :param domain: str
            any domain, example "youtube.com"
        :return: Bool
            True if success, False if fail
        """
        return WebsiteOpen.website_opener(domain)

    def launch_any_app(self, path_of_app=r'C:\Program Files\Mozilla Firefox\firefox.exe'):
        """
        Launch any windows application according to application path.

        :param path_of_app: str
            path of exe

        :return: Bool
            True if success and open the application, False if fail
        """
        return OpenApp.launch_app(path_of_app)

    def shutdown(self):
        """
        Shutdown the Jarvis API, exit from program.

        :return: None/bool
            if no error then exit from program, False if Fail
        """
        try:
            self.text2speech('Good bye. Have a nice day')
            sys.exit()
        except Exception as e:
            print(e)
            return False

    def setup(self):
        """
        Method to define configuration related to assistant.

        :return: Bool
            True if setup done
            False if setup cancel or interrupt
        """
        obj_setup = Setup()
        response = obj_setup.setup_assistant()
        del obj_setup
        return response

    def tell_me(self, topic='India'):
        """
        Tells about anything from wikipedia in summary.

        :param topic: str
            any string is valid options

        :param sentences: int
            number of sentence

        :return: str
            Summary of topic
        """
        try:
            obj = Wikipedia()
            res = obj.tell_me_about(topic)
        except Exception as e:
            print(e)
            res = False
        return res

    def screenshot_(self):
        """
        Save the screenshot.
        """
        image = pyautogui.screenshot()
        date = datetime.datetime.now().strftime("%b-%d")
        time = datetime.datetime.now().strftime("%I-%M-%S")
        image.save(
            f'images\/{date}-{time}.png')


if __name__ == '__main__':
    obj = Jarvis()
