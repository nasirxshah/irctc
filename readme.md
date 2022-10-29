### API USAGE

```python
from irctc.api import LoginAPI
from irctc.captcha import LoginCaptcha, CaptchaExtractor
from irctc.payload import WebTokenPayload
import logging
logging.basicConfig(level=logging.DEBUG)

api = LoginAPI()
r = api.initCaptcha()

captcha = LoginCaptcha(r['nlpKeyValue'])
extractor = CaptchaExtractor(captcha.generate_nlpimg())
print(extractor.getCaptcha())
nlpans = input("enter solution: ")

payload = WebTokenPayload("your_username", "your_password", r["status"])
api.generateAccessToken(payload.captchawebtoken(
    r["nlpKeyValue"], extractor.nlpIdentifier(), nlpans))
api.generateCsrfToken()
```