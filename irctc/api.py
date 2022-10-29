from asyncio.log import logger
from urllib.parse import urljoin
from ._request import ISession
from .helper import timeStamp, validateResponse
from requests.cookies import RequestsCookieJar
import logging
logger = logging.getLogger("IRCTC")


class API:
    _default_root_uri = "https://www.irctc.co.in"
    _routes = {
        "train.avlenq": "/eticketing/protected/mapps1/altAvlEnq/TC",
        "booking.fareenq": "/eticketing/protected/mapps1/avlFarenquiry/{trainNumber}/{journeyDate}/{fromStnCode}/{toStnCode}/{classCode}/{quotaCode}/N",
        "user.masterlist": "/eticketing/protected/mapps1/masterpsgnlistenquiry",
        "booking.boardingenq": "/eticketing/protected/mapps1/boardingStationEnq",
        "booking.lapfareenq": "/eticketing/protected/mapps1/allLapAvlFareEnq/Y",
        "booking.otp.resend": "/eticketing/protected/mapps1/resendOTP/BOOKING",
        "booking.otp.confirm": "/eticketing/protected/mapps1/captchaverify/{txnid}/BOOKINGWS/{otp}",
        "booking.captcha.confirm": "/eticketing/protected/mapps1/nlpcaptchaverify/{txnid}/BOOKINGWS/{nlpanswer}",
        "booking.captcha.exception.confirm": "/eticketing/protected/mapps1/nlpcaptchaverify/{txnid}/BOOKINGWS/{nlpAnswer}",
        "payment.init": "eticketing/protected/mapps1/bookingInitPayment/{txnid}",
        "payment.ewallet.confirm": "eticketing/protected/mapps1/verifyPayment/{txnid}",
        "payment.ewallet.otp.resend": "/eticketing/protected/mapps1/resendPaymentOtp/{txnid}",
        "payment.redirect": "/eticketing/PaymentRedirect"
    }

    def __init__(self, bearer_token, csrf_token, uid, debug=False, timeout=None, cookies=RequestsCookieJar()) -> None:
        self.session = ISession(
            bearer_token, csrf_token, uid, debug=debug, timeout=timeout, cookies=cookies)
        self._default_headers = "auth.csrf.uid.ctype"

    def getAvlTrains(self, payload):
        resp = self._post("train.avlenq", json=payload)
        return resp

    def enqSeatAvl(self, payload):
        url_args = {
            "trainNumber": payload["trainNumber"],
            "journeyDate": payload["journeyDate"],
            "fromStnCode": payload["fromStnCode"],
            "toStnCode": payload["toStnCode"],
            "classCode": payload["classCode"],
            "quotaCode": payload["quotaCode"]
        }
        resp = self._post("booking.fareenq", url_args=url_args,
                          json=payload)
        return resp

    def getBoardingstns(self, payload):
        resp = self._post("booking.boardingenq", json=payload)
        return resp

    def getFarePrice(self, payload):
        resp = self._post("booking.lapfareenq", json=payload)
        return resp

    def initPayment(self, txnid, payload):
        params = {"insurenceApplicable": "NA"}
        resp = self._post("payment.init", url_args={
            "txnid": txnid}, params=params, json=payload)
        return resp

    def confirmBookingCaptcha(self, txnid, nlpKeyValue, nlpIdentifier, nlpAnswer):
        url_args = {
            "txnid": txnid,
            "nlpanswer": nlpAnswer
        }
        payload = {"nlpToken": nlpKeyValue,
                   "nlpType": "BOOKING",
                   "nlpAnswer": nlpAnswer,
                   "nlpIdentifier": nlpIdentifier}
        resp = self._post("booking.captcha.confirm",
                          url_args=url_args, json=payload)
        return resp

    def _post(self, route, url_args=None, data=None, json=None, params=None, headers=""):
        url = self._makeurl(route, url_args=url_args)
        return validateResponse(self.session.post(url, data=data, json=json, params=params, _headers=headers if headers else self._default_headers))

    def _makeurl(self, route, url_args=None):
        if url_args:
            uri = self._routes[route].format(**url_args)
        else:
            uri = self._routes[route]

        return urljoin(self._default_root_uri, uri)


class LoginAPI:
    _default_root_uri = "https://www.irctc.co.in"
    _routes = {
        "login.txttonum": "/eticketing/protected/profile/textToNumber/{timestamp}",
        "login.sensor": "/wz_9t8/8LzDU/hI812/OUZ1/7f5Srb6J5b/KyMEeFx7bw/Ukg5/VUwAU1wB",
        "login.otp": "/eticketing/protected/mapps1/resendOTP/LOGIN",
        "login.otp.confirm": "/eticketing/protected/mapps1/validateUser",
        "login.captcha": "/eticketing/protected/mapps1/loginCaptcha",
        "login.webtoken": "/authprovider/webtoken",
        "login.csrftoken": "/eticketing/protected/mapps1/validateUser",
        "logout": "/eticketing/protected/mapps1/logout",
    }

    def __init__(self, debug=False, timeout=None, cookies=RequestsCookieJar()) -> None:
        self.session = ISession(
            debug=debug, timeout=timeout, cookies=cookies)

    def _texttonumber(self):
        return self._get("login.txttonum", url_args={"timestamp": timeStamp()}, headers="uid.bmirak")

    def _validatesensor(self):
        payload = {
            "sensor_data": "2;4277317;3687224;19,0,0,0,4,0;nL+k_ihvcl,Z%Fqa?G6LAagT>2St5E@sA|uXT>ArV~VJ@lk6xHO:SL4&pkN03dm.{XVOD9+navr&X=^s%;3NZnAS37V=l ] #lem7;g^LqGcX`FSh|&:>u!:ufBHN[2ZS:9_* 3!/f@UdA|xx.[Af )VVeG.DV1b]Riotmwk7RzBL.tQ-A[49ouE8>+pd|lq_On*057?i cs`~ayEL[,H0=VcvmD`.)OYTwt:D]TW=%rmTi:lSLc5^&# <@Qo8-<DFmo5Afju_GY(d(;E|t!D7M!;M?;m*y3Q1]W/Vcf~y 4VZoH-z$w@%D|5bUV$OO3R`1Zp(Je,wtEsyw=[<dMsf2o<VA29bVZ?.QM6DMSpdqD&)/Ur]2#MNxa~x-NY9po4PsJCIy,)X[7D.~cOn@=-nJ+V_;I-*I&]^/iIn=gJ7?#hnE/55MY4.9o/joMFd%vDgwM-fK.8OO51cqc.vc_Q~2)plR#J@K`9eHunP|J%1J>%?XozjS1XLAA,4!E|w2P<T@j+m/j3IlcRr6$WVH*QQS]~p-YJRk$_=/Zb4-]DZ,9sDcG.?49AiCB%m:)BoAD48j;?+)YJd/X2V: :ki;gw0 0SKw  KmgCUFWCGPntT8TjzF<BYfm5 6meH|yv!VTYYILeM!|W -)i=>9BS5}@t,[P}Yr ^!=Au|r.I`q{kv%!oHJS]R=Yl0,-jRwlSyx?#s*,=~C+?^hB/.-l24b{+wMY^W@e9nFu|(899MP&m+4IH*;LB;S+8BOTfSc)w`k]vz/^4Vx8.FjaUXd:W0P4AjyU%eJ2QK>[6qA2bgdL>_`*vLvnDe@+6vzni^-#lWh?DFw#R]ij#w[=2(t;+~&x+e44<*gA(|3Cv!Ua-5cbD|KJfl$i5C_7G+Feu5^3!x6]e5U(D}x ?E~Q4NpiQ~_;~_IPGO8hj:Y5RbH0AKsG,_>^Px8M<ZK,dN~Gae?w/0`{]nX&a{TI!|DxZjJ(glLI%|uw$:$g7QR*R5?7.1n0!lKk8_8|fsgR:+WAJltC[^EyOwcui}+&QN}EO4lfWZQKWj{lh-!(1D/N7{q<,m.JcdXm6ibV@M=H<=*y858*?;`-*}-K5v90;!;;V>5&(]2sd9 4C+4c.@<RyfXssOxFg;2YuaeC|r,i q +YrEaxmMy6|kn9Q5cs[i`[y[%4WJX;GMrYqIC~2QWN~ZDpAwQtz2MM3R$Hl^s?Kvv!q?s&$;JOGl#jA!+JR9Z=Ve})gj8PVQ:5ws+?lrO@BMZYj+H`&k6/ iNnLC%o-:4 DfxqE`xTX<hVo4*5Et,7~uI^0{b2wvsu+ gMe jQTtv[3ov6$i-l3+f-uyuJ`6#M+03b)+m_kQhWDpN&h3)m7[.QW-f85&_@Tl5qoQ5@6sxlA}D/6_NHBG&|@3bxC7@l;AfqK=8XuR`A&n$]vCVPX7ly!@/.DSrtj<26f**m5JaxBi_BX|=KW^WV%Wj4_;cWtA~5#<QD-{cj4uAc9P6JZD+7pRi2%w#ds7hJc0Hnvm&m#;YkB<mO1?PDod@*wI)0EAr~&GrS|]4z@ir.8]i$&*{e.MEE[aEEok:NW0SAke0vGs*=2vAK.YO@|>B/Mi@VHlSqRo%6}I5^M>*^,0apR%,rS&&7EZVV#!n6E1nP+xcS%g}FS8U}jfQARi9eo83X)$v8cF|nZP7&`up.7Cd/nb#` o8T@vpgsu-uk[(~1Ncn0|u~x/czy^yz83|a[n)0cTCi40e.A`!6YC!Ykl9s@dqwBD1H78zZaGK$xF*7+83?{zKyHj-iSnIzSQ *@5CvlkvV2DT+53*C&A9DsfSV:;^19F$GQGWSM>c.h}]yr-3C>30&~Juu:xCG}3g{Ftb=T)ni7@-R#tx:=0s{]MN{29 Mh1R}YFhMCp+pT[(-+[w~u-y{#R9Juf9MH)6n#V*QPc97n&w=^(-N[haQ~l|:rdN(NyW6xuA&/)+%pG7dn!>)+BEaq5;x^{a(dBNS2Eq*iJw})%;f%pxS]#/pNs1;UtG)2SDokGKVI1qa`|L?-&(BIn<D}Kc(6eC)nLB>4>wc5*:U=b!e)g:#%TO"
        }
        return self._post("login.sensor", json=payload)

    def initCaptcha(self, exception=False):
        self._texttonumber()
        self._validatesensor()
        params = {"nlpCaptchaException": True} if exception else None
        resp = self._get("login.captcha", params=params, headers="uid.bmirak")
        data = validateResponse(resp)
        self.session.uid = data.get("status")
        return data

    def generateAccessToken(self, payload):
        resp = self._post("login.webtoken", data=payload,
                          headers="bmirak.ctype")
        data = validateResponse(resp)
        self.session.bearer_token = data.get("access_token")
        logger.debug(f"access token: {data.get('access_token')}")
        return data

    def generateCsrfToken(self):
        params = {"source": 3}
        resp = self._get("login.csrftoken", params=params,
                         headers="auth.csrf.uid.bmirak")
        logger.debug(f"csrf token: {resp.headers.get('csrf-token')}")
        return resp.headers.get("csrf-token")

    def _get(self, route, url_args=None, params=None, headers=""):
        url = self._makeurl(route, url_args=url_args)
        return self.session.get(url, params=params, _headers=headers)

    def _post(self, route, url_args=None, data=None, json=None, params=None, headers=""):
        url = self._makeurl(route, url_args=url_args)
        return self.session.post(url, data=data, json=json, params=params, _headers=headers)

    def _makeurl(self, route, url_args=None):
        if url_args:
            uri = self._routes[route].format(**url_args)
        else:
            uri = self._routes[route]

        return urljoin(self._default_root_uri, uri)
