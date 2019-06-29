import hashlib


class Generator(object):
    __GRAVATAR_DEFAULT_URL: str = "https://upload.wikimedia.org/wikipedia/commons/f/f4/User_Avatar_2.png"
    __GRAVATAR_DEFAULT_SIZE: int = 600

    @staticmethod
    def gravatar_url(email: str) -> str:
        return "https://www.gravatar.com/avatar/" + hashlib.md5(
            email.lower().encode()).hexdigest() + "?" + f"s={Generator.__GRAVATAR_DEFAULT_SIZE}" + "&" + f"d={Generator.__GRAVATAR_DEFAULT_URL}"
