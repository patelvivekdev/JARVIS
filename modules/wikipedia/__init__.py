import wikipedia
import string


class Wikipedia:
    def __init__(self) -> None:
        pass

    def tell_me_about(topic, sentences):
        try:
            res = wikipedia.summary(title=string.capwords(
                topic), sentences=sentences, auto_suggest=False)
            return res
        except Exception as e:
            print(e)
            return False
