import wikipedia
import string


class Wikipedia:
    def __init__(self) -> None:
        pass

    def tell_me_about(self, topic):
        try:
            res = wikipedia.summary(title=string.capwords(topic),
                                    auto_suggest=False)
            return res
        except Exception as e:
            print(e)
            return False
