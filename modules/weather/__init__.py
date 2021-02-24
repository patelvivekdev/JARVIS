import requests


class Weather:
    def __init__(self):
        pass

    def get_temperature(self, json_data):
        temp_in_celcius = json_data['main']['temp']
        return temp_in_celcius

    def get_weather_type(self, json_data):
        weather_type = json_data['weather'][0]['description']
        return weather_type

    def get_wind_speed(self, json_data):
        wind_speed = json_data['wind']['speed']
        return wind_speed

    def get_weather_data(self, json_data, city):
        weather_type = self.get_weather_type(json_data)
        temperature = self.get_temperature(json_data)
        wind_speed = self.get_wind_speed(json_data)
        return f"The weather in {city} is currently {weather_type} with a temperature of {temperature} Celsius and wind speeds reaching {wind_speed} km/ph"

    def main_weather(self, city):
        """
        City to weather
        :param city: City
        :return: weather
        """

        api_address = f'https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid=62acd2d2a6e9a1b6e8cf3af2d2545dea'
        try:
            json_data = requests.get(api_address).json()
            if not json_data == 0:
                weather_details = self.get_weather_data(json_data, city)

                return weather_details
            else:
                raise ValueError
        except Exception as e:
            print("Please Enter name of city")
            return None

    def weather_app(self, city):
        weather_res = self.main_weather(city)
        return weather_res


if __name__ == '__main__':
    obj = Weather()
