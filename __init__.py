# Import Tools
import os

# Import Custom module
from JARVIS.modules.face_identification import FaceRecognition
from JARVIS.modules.weather import Weather
from JARVIS.modules.date import Date
from JARVIS.modules.time import Time
from JARVIS.modules.setup import Setup


class Jarvis:
    def _init__(self):
        pass

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
