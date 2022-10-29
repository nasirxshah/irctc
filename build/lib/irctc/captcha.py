import requests
import json
import base64
from urllib.parse import urljoin
from .helper import timeStamp
import re
from bs4 import BeautifulSoup
from .payload import CaptchaPayload


class NlpCaptcha():
    _default_root_uri = "https://irctclive.nlpcaptcha.in"
    _routes = {
        "nlpimg.gen": "/index.php/nlpgen/nlpimg/fetch/{encoded_nlpoptions}"
    }

    def __init__(self) -> None:
        self._refresh_count = 0
        self.reqsession = requests.Session()
        self._payload = CaptchaPayload()

    def refresh(self):
        self._refresh_count += 1

    @property
    def nlpoptions(self):
        self._nlpoptions.t = timeStamp()
        if self._refresh_count:
            self._nlpoptions.mandatorytype = ""
            self._nlpoptions.nlpRefCnt = str(self._refresh_count)
            self._nlpoptions.theme_size = "300x270"
        return self._nlpoptions.__dict__

    def generate_nlpimg(self):
        url = urljoin(self._default_root_uri, self._routes["nlpimg.gen"].format(
                      encoded_nlpoptions=self.btoa(self.nlpoptions)))
        r = self.reqsession.get(url)
        return r.content.decode()

    @staticmethod
    def btoa(object):
        object_str_encoded = json.dumps(object, separators=(',', ":")).encode()
        object_encode_decoded = base64.b64encode(s=object_str_encoded).decode()
        return object_encode_decoded


class LoginCaptcha(NlpCaptcha):
    def __init__(self, nlpkeyvalue) -> None:
        super().__init__()
        self._nlpoptions = self._payload.loginOptions(nlpkeyvalue)


class BookingCaptcha(NlpCaptcha):
    def __init__(self, nlpkeyvalue, fromStn, toStn, jrnyDate, arivalDate, classcode, quota, trainType, user_age, user_gender) -> None:
        super().__init__()
        self._nlpoptions = self._payload.bookingOptions(
            nlpkeyvalue, fromStn, toStn, jrnyDate, arivalDate, classcode, quota, trainType, user_age, user_gender)


class CaptchaExtractor:
    def __init__(self, content) -> None:
        self.content = content
        self._step1()
        self._step2()

    def _step1(self):
        self.content = re.findall('".*"', self.content)[0]

    def _step2(self):
        self.content = re.sub(r"\\n", "\n", self.content)
        self.content = re.sub(r"\\t", "\t", self.content)
        self.content = re.sub(r'\\"', '"', self.content)
        self.content = re.sub(r"\\/", "/", self.content)

    def nlpIdentifier(self):
        soup = BeautifulSoup(self.content, features="html.parser")
        item = soup.find(id="nlpIdentifier")
        return item.get('value')

    def getCaptcha(self):
        soup = BeautifulSoup(self.content, features="html.parser")
        container = soup.find(id="nlpImgContainer")
        images = list(
            map(lambda image: image['src'], container.find_all('img')))
        if images:
            return images[-1]
        else:
            raise Exception("> Captcha Image Not Found!")
