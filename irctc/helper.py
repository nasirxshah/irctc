from time import time_ns
from datetime import datetime
import base36
from .exceptions import *
from requests import Response


def timeStamp() -> str:
    return str(time_ns()//1000000)


def dateTimeStamp() -> str:
    now = datetime.now()
    return f"{str(now.date())}T{now.time()}"[:-3]


def base36TimeStamp() -> str:
    return base36.dumps(time_ns()//1000000)


def validateResponse(response: Response) -> dict[str, Any] | str | bytes:
    if "application/json" in response.headers["content-type"]:
        try:
            data = response.json()
        except ValueError:
            raise DataException({"statement": ["couldn't parse the JSON response received from the server"],
                                 "content": [response.content]
                                 })
        return data
    elif "text/html" in response.headers["content-type"]:
        return response.content.decode('utf-8')
    elif "application/javascript" in response.headers["content-type"]:
        return response.content.decode('utf-8')
    elif "image/jpeg" in response.headers["content-type"]:
        return response.content
    elif "text/plain" in response.headers["content-type"]:
        return str(response.content)
    else:
        raise DataException({"statement": ["unknown Content-Type"],
                             "content-type": [response.headers["content-type"]],
                             "content": [response.content]
                             })
