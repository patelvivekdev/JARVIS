import datetime


class Date:
    def __init__(self) -> None:
        pass

    def date():
        """
        Just return date as string
        :return: date if success, False if fail
        """
        try:
            date = datetime.datetime.now().strftime("%b %d %Y")
        except Exception as e:
            print(e)
            date = False
        return date


if __name__ == '__main__':
    obj = Date()
