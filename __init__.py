# Import Tools
import os

# Import Custom module
from JARVIS.modules.face_identification import FaceRecognition
from JARVIS.modules.weather import Weather


class Jarvis:
    def _init__(self):
        pass

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


if __name__ == '__main__':
    obj = Jarvis()
