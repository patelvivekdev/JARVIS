import datetime


class Time:
    def __init__(self) -> None:
        pass

    def time():
        """
        Just return date as string
        :return: time if success, False if fail
        """
        try:
            time = datetime.datetime.now().strftime("%I:%M:%S")
        except Exception as e:
            print(e)
            time = False
        return time


if __name__ == '__main__':
    obj = Time()
