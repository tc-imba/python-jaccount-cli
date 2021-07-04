from datetime import datetime
from io import BytesIO
from types import TracebackType
from typing import Optional, Type, Dict, Any
from http.cookies import SimpleCookie
from urllib.parse import urlparse

from aiohttp import ClientSession
from bs4 import BeautifulSoup
from jaccount_cli.ascii import ImageToAscii, Image

# make the jaccount server believe it is a browser
JACCOUNT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/91.0.4472.77 Safari/537.36",
    "Accept-Language": "zh-CN,zh;q=0.9",
}
CAPTCHA_URL = "https://jaccount.sjtu.edu.cn/jaccount/captcha"
LOGIN_URL = "https://jaccount.sjtu.edu.cn/jaccount/ulogin"


class JaccountCLIAsyncIO:
    def __init__(self, base_url: str, session: Optional[ClientSession] = None):
        if session:
            self.session = session
            self._session_autoclose = False
        else:
            self.session: ClientSession = ClientSession(headers=JACCOUNT_HEADERS)
            self._session_autoclose = True
        self.base_url: str = base_url
        self.cookies: Optional[SimpleCookie[str]] = None
        self.captcha_image: Optional[Image] = None
        self.params: Dict[str, Any] = {}

    async def __aenter__(self) -> "JaccountCLIAsyncIO":
        return self

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]],
        exc_val: Optional[BaseException],
        exc_tb: Optional[TracebackType],
    ) -> None:
        if self._session_autoclose:
            await self.session.close()

    async def init(self):
        async with self.session.get(self.base_url) as response:
            body = await response.text()
            self.cookies = response.cookies
        soup = BeautifulSoup(body, "html.parser")
        hidden_inputs = soup.select("input[type=hidden]")
        self.params = dict({(x["name"], x["value"]) for x in hidden_inputs})
        url = "%s?uuid=%s&t=%d" % (
            CAPTCHA_URL,
            self.params["uuid"],
            int(datetime.now().timestamp()),
        )
        async with self.session.get(url, cookies=self.cookies) as response:
            fp = BytesIO()
            fp.write(await response.read())
            self.captcha_image = fp

    async def login(self, username, password, captcha):
        self.params["v"] = ""
        self.params["user"] = username
        self.params["pass"] = password
        self.params["captcha"] = captcha

        async with self.session.post(
            LOGIN_URL, cookies=self.cookies, data=self.params
        ) as response:
            pass

    def captcha_show_external(self):
        image = Image.open(self.captcha_image)
        image.show()

    def captcha_generate_ascii(self):
        image_to_ascii = ImageToAscii(self.captcha_image)
        return image_to_ascii.clean()

    def get_cookies(self):
        url = urlparse(self.base_url)
        domain_url = "{}://{}".format(url.scheme, url.netloc)
        cookies = self.session.cookie_jar.filter_cookies(domain_url)
        return cookies
