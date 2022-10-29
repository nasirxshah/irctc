import logging
from typing import Any
from requests import Session, Response
from requests.cookies import RequestsCookieJar
from irctc.helper import timeStamp
from .exceptions import *


logger = logging.getLogger("IRCTC")
logging.getLogger('urllib3').setLevel(level=logging.WARNING)


class ISession(Session):
    _default_timeout = 7

    def __init__(self, bearer_token=None, csrf_token=None, uid=None, debug=False, timeout=None, cookies=RequestsCookieJar()) -> None:
        super().__init__()
        self.bearer_token = bearer_token
        self.csrf_token = csrf_token
        self.uid = uid
        self.debug = debug
        self.timeout = timeout if timeout else self._default_timeout
        self.cookies.update(cookies)

        self._user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/105.0.0.0 Safari/537.36"

    def get(self, url, params=None, _headers="") -> Response:
        headers = self._make_headers(_headers)
        if self.debug:
            logger.debug("Request: \n\t> {method}\n\t> {url}\n\t> {params}\n\t> {headers}".format(
                method="GET", url=url, params=params, headers=headers))
        resp = super().get(url, params=params, headers=headers, timeout=self.timeout)
        if self.debug:
            logger.debug("Response:\n\t> {code}\n\t> {content}".format(
                code=resp.status_code, content=resp.content))
        if "spa-csrf-token" in headers:
            self.csrf_token = resp.headers.get('csrf-token')
        return resp

    def post(self, url, data=None, json=None, params=None, _headers=""):
        headers = self._make_headers(
            _headers, content_type="json" if json else "form")

        if self.debug:
            logger.debug("Request: \n\t> {method}\n\t> {url}\n\t> {params}\n\t> {headers}".format(
                method="POST", url=url, params=json if json else data, headers=headers))

        resp = super().post(url, data=data, json=json, params=params,
                            headers=headers, timeout=self.timeout)

        if self.debug:
            logger.debug("Response:\n\t> {code}\n\t> {content}".format(
                code=resp.status_code, content=resp.content))

        if "spa-csrf-token" in headers:
            self.csrf_token = resp.headers.get('csrf-token')
        return resp

    def _make_headers(self, _headers="", content_type=None):
        headers = {}
        if _headers:
            for header in _headers.split("."):
                if header == "auth":
                    if self.bearer_token:
                        headers["Authorization"] = f"Bearer {self.bearer_token}"
                    else:
                        raise InvalidInputException(
                            {"statement": ["bearer token missing"]})
                elif header == "csrf":
                    if self.csrf_token:
                        headers["spa-csrf-token"] = self.csrf_token
                    else:
                        headers["spa-csrf-token"] = timeStamp()
                elif header == "uid":
                    if self.uid:
                        headers["greq"] = self.uid
                    else:
                        headers["greq"] = timeStamp()

                elif header == "bmirak":
                    headers["bmirak"] = "webbm"

                elif header == "ctype":
                    if content_type == "json":
                        headers[header] = "aplication/json"
                    elif content_type == "form":
                        headers[header] = "application/x-www-form-urlencoded"
                    else:
                        raise InvalidInputException(
                            {"statement": ["content-type not defined"]})
                else:
                    raise InvalidInputException({"statement": ["header not found in headers map",
                                                               "or it might not be supported"]})
        headers["User-Agent"] = self._user_agent
        return headers

