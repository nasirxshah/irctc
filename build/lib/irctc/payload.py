from ._models import *
from .helper import *
from dataclasses import asdict
from .exceptions import PayloadException
import base64


class WebTokenPayload:
    def __init__(self, username, password, uid) -> None:
        self.webtokenpayload = WebTokenModel()
        self.webtokenpayload.grant_type = "password"
        self.webtokenpayload.username = username
        self.webtokenpayload.password = base64.b64encode(
            password.encode()).decode()
        self.webtokenpayload.uid = uid
        self.webtokenpayload.lso = ""
        self.webtokenpayload.encodedPwd = True

    def otpwebtoken(self):
        self.webtokenpayload.captcha = ""
        self.webtokenpayload.otpLogin = True
        self.webtokenpayload.nlpIdentifier = ""
        self.webtokenpayload.nlpAnswer = ""
        self.webtokenpayload.nlpToken = ""
        return asdict(self.webtokenpayload)

    def captchawebtoken(self, nlpToken, nlpIdentifier, nlpAnswer):
        self.webtokenpayload.captcha = ""
        self.webtokenpayload.otpLogin = False
        self.webtokenpayload.nlpIdentifier = nlpIdentifier
        self.webtokenpayload.nlpAnswer = nlpAnswer
        self.webtokenpayload.nlpToken = nlpToken
        return asdict(self.webtokenpayload)

    def specialwebtoken(self, captcha):
        self.webtokenpayload.captcha = captcha
        self.webtokenpayload.otpLogin = False
        self.webtokenpayload.nlpIdentifier = ""
        self.webtokenpayload.nlpAnswer = ""
        self.webtokenpayload.nlpToken = ""
        return asdict(self.webtokenpayload)


class BookingPayload:
    Payment_Type_UPI = '2'
    Payment_Type_BANK = '3'

    Class_SLEEPER = "SL"
    Class_SECOND_SITTING = "2S"
    Class_3_TIER = "3A"
    Class_2_TIER = "2A"
    Class_FIRST_CLASS = "1A"

    Quota_GENERAL = "GN"
    Quota_TATKAL = "TQ"
    Quota_PREMIUM_TATKAL = "PT"
    Quota_LADIES = "LD"
    Quota_SENIOR_CITIZEN = "SS"
    Quota_PHYSICALLY_DISABLED = "HP"

    Train_Type_OTHER = "O"
    Train_Type_SPECIAL = "SP"
    Train_Type_SPECIAL_TATKAL = "ST"
    Train_Type_RAJDHANI = "R"
    Train_Type_DURONTO = "D"

    Gender_MALE = "M"
    Gender_FEMALE = "F"

    def __init__(self,
                 user_name: str,
                 from_stn: str,
                 to_stn: str,
                 jrny_date: str,
                 quota,
                 class_code,
                 train_no: str,
                 mobile: str,
                 train_type,
                 travel_days: int,

                 payment_type
                 ) -> None:

        self.username: str = user_name

        self.fromStation: str = from_stn
        self.toStation: str = to_stn
        self.jrnyDate: str = jrny_date
        self.quota: str = quota
        self.classcode: str = class_code
        self.trainNo: str = train_no
        self.mobile: str = mobile
        self.passengers: list[Passenger] = []
        self.trainType: str = train_type
        self.travelDays: int = travel_days

        self.paymentType: str = payment_type
        self.psgn_count = 0

    def addPassenger(self, name, age, gender):
        self.psgn_count += 1
        passenger = Passenger()
        passenger.passengerName = name
        passenger.passengerAge = age
        passenger.passengerGender = gender
        passenger.passengerSerialNumber = self.psgn_count
        self.passengers.append(passenger)

    @property
    def avltrainenq(self):
        payload = TrainAvlEnqModel()
        # unresolved
        payload.concessionBooking = False
        payload.jrnyClass = ""
        payload.currentBooking = "false"
        payload.flexiFlag = False
        payload.handicapFlag = False
        payload.ticketType = "E"
        payload.loyaltyRedemptionBooking = False
        payload.ftBooking = False

        # resolved
        payload.srcStn = self.fromStation
        payload.destStn = self.toStation
        payload.jrnyDate = self.jrnyDate
        payload.quotaCode = self.quota
        return asdict(payload)

    @property
    def trainfareenq(self):
        payload = TrainFareModel()

        # unresolved
        payload.paymentFlag = "N"
        payload.concessionBooking = False
        payload.ftBooking = False
        payload.loyaltyRedemptionBooking = False
        payload.ticketType = "E"
        # mid - resolved
        payload.isLogedinReq = True

        # resolved
        payload.quotaCode = self.quota
        payload.trainNumber = self.trainNo
        payload.fromStnCode = self.fromStation
        payload.toStnCode = self.toStation
        payload.journeyDate = self.jrnyDate
        payload.classCode = self.classcode
        payload.moreThanOneDay = True  # TODO
        payload.returnJourney = False
        payload.returnTicket = False

        return asdict(payload)

    @property
    def boardingstn(self):
        payload = BoardingModel()
        # unresolved
        payload.clusterFlag = "N"
        payload.onwardFlag = "N"
        payload.cod = "false"
        payload.gnToCkOpted = False
        payload.twoPhaseAuthRequired = False
        payload.captureAddress = 0
        payload.passBooking = False
        payload.journalistBooking = False

        # mid-resolved
        payload.paymentType = 1
        payload.autoUpgradationSelected = False

        # resolved
        payload.reservationMode = "WS_TA_B2C"
        payload.alternateAvlInputDTO = []
        payload.returnJourney = False
        payload.returnTicket = False

        # functional
        altdto = AltDTO()
        altdto.srcStn = self.fromStation
        altdto.destStn = self.toStation
        altdto.jrnyDate = self.jrnyDate
        altdto.jrnyClass = self.classcode
        altdto.quotaCode = self.quota
        altdto.trainNo = self.trainNo
        payload.alternateAvlInputDTO.append(altdto)

        return asdict(payload)

    @property
    def lapfareenq(self):
        payload = LapFareModel()

        # unresolved
        payload.clusterFlag = "N"
        payload.onwardFlag = "N"
        payload.cod = "false"
        payload.gnToCkOpted = False
        payload.twoPhaseAuthRequired = False
        payload.captureAddress = 0
        payload.ticketType = "E"
        payload.mainJourneyTxnId = None
        payload.mainJourneyPnr = ""
        payload.captcha = ""
        payload.ftBooking = False
        payload.loyaltyRedemptionBooking = False
        payload.nosbBooking = False
        payload.warrentType = 0
        payload.ftTnCAgree = False
        payload.returnJourney = False
        payload.connectingJourney = False
        payload.gstDetails = {
            "gstIn": "",
            "error": None
        }

        # mid- resolved
        payload.generalistChildConfirm = False
        payload.autoUpgradationSelected = False
        payload.paymentType = self.paymentType
        payload.bookingChoice = 1
        payload.bookingConfirmChoice = 1
        payload.bookOnlyIfCnf = False
        # resolved
        payload.reservationMode = "WS_TA_B2C"
        payload.wsUserLogin = self.username
        payload.moreThanOneDay = False  # TODO
        payload.boardingStation = self.fromStation
        payload.reservationUptoStation = self.toStation
        payload.mobileNumber = self.mobile

        # functional
        payload.clientTransactionId = base36TimeStamp()

        lapdto = LapDTO()
        # unresolved
        lapdto.coachId = None
        lapdto.travelInsuranceOpted = False  # todo
        lapdto.warrentType = 0
        lapdto.coachPreferred = False
        lapdto.addMealInput = None
        lapdto.concessionBooking = False
        lapdto.ssQuotaSplitCoach = "N"
        # mid-resolved
        lapdto.ignoreChoiceIfWl = True
        lapdto.reservationChoice = "99"
        lapdto.autoUpgradation = False
        lapdto.bookOnlyIfCnf = False

        # resolved
        lapdto.trainNo = self.trainNo
        lapdto.journeyDate = self.jrnyDate
        lapdto.fromStation = self.fromStation
        lapdto.toStation = self.toStation
        lapdto.journeyClass = self.classcode
        lapdto.quota = self.quota
        lapdto.passengerList = self.passengers  # todo

        payload.lapAvlRequestDTO = []
        payload.lapAvlRequestDTO.append(lapdto)

        return asdict(payload)

    def ewalletpaymentconfirm(self, amount: str, otp: int, serverid: str):
        payload = {
            "amount": amount,
            "bankId": "0",
            "loyaltyNum": "0",
            "paramList": [
                {
                    "key": "OTP",
                    "value": otp
                },
                {
                    "key": "TXN_TYPE",
                    "value": "undefined"
                }
            ],
            "remainingBalance": "0.0",
            "serverId": serverid,
            "timeStamp": dateTimeStamp(),
            "transationId": "0",
            "txnDate": dateTimeStamp(),
            "txnStatus": "12",
            "txnType": "0",
            "upiModeOpted": "0"
        }
        return payload


class PaymentPayload:
    Paytm = "117"
    TxnType_Paytm = 1

    IRCTC_eWallet = 1000
    TxnType_IRCTC_eWallet = 7

    def __init__(self, amount, gateway) -> None:
        self.amount = amount
        self.gateway = gateway

    @property
    def paymentinit(self):
        """{'bankId':'117','txnType':1,'paramList':[],'amount':'421.8','transationId':0,'txnStatus':1}"""
        _p = {
            "amount": self.amount,
            "bankId": self.gateway,
            "transationId": 0,
            "txnStatus": 1,
            "paramList": []

        }

        if self.gateway == self.Paytm:
            _p["txnType"] = self.TxnType_Paytm

        elif self.gateway == self.IRCTC_eWallet:
            _p["txnType"] = self.TxnType_IRCTC_eWallet
            _p["paramList"].append({
                "key": "TXN_PASSWORD",
                "value": ""
            })
        return _p


class CaptchaPayload:
    _default_key_login = "125fc0fca3c84336ae0000dc2933d300"
    _default_key_booking = "f2c5d744485b0b4251461454db791111"

    def __init__(self) -> None:
        self.ajax = 1
        self.ajaxContainer = "ShowNLPCaptcha"
        self.html5audio = "wav"

    def loginOptions(self, nlpkeyvalue):
        payload = NlpOptions()
        payload.ajax = self.ajax
        payload.ajaxContainer = self.ajaxContainer
        payload.html5audio = self.html5audio
        payload.key = self._default_key_login
        payload.token = nlpkeyvalue
        payload.t = timeStamp()

        return payload

    def bookingOptions(self, nlpkeyvalue, fromStn, toStn, jrnyDate, arivalDate, classcode, quota, trainType, user_age, user_gender):
        payload = BookingNlpOptions()
        payload.ajax = self.ajax
        payload.ajaxContainer = self.ajaxContainer
        payload.html5audio = self.html5audio
        payload.key = self._default_key_booking
        payload.token = nlpkeyvalue
        payload.t = timeStamp()

        payload.irctc_from_station_code = fromStn
        payload.irctc_to_station = toStn
        payload.irctc_journey_date = jrnyDate
        payload.irctc_arrival_date = arivalDate
        payload.irctc_class_code = classcode
        payload.irctc_quota = quota
        payload.irctc_train_type = trainType
        payload.irctc_age = user_age
        payload.irctc_gender = user_gender

        return payload


class PayloadChecker:
    _default_passenger_name_max_length = 16
    _default_passenger_max_age = 125
    _default_passenger_min_age = 1

    def __init__(self, payload: BookingPayload) -> None:
        self.payload = payload
        self.errors = []

    def check_all(self):
        self.empty_passenger_list()
        self.invalid_age()
        self.invalid_gender()
        self.invalid_class()
        self.invalid_date()
        self.invalid_name()
        self.invalid_quota()
        self.invalid_mobile()
        self.invalid_paymentType()
        if self.errors:
            raise PayloadException(*self.errors)
        return True

    def empty_passenger_list(self):
        if not self.payload.passengers:
            self.errors.append("Empty Passenger List")

    def invalid_gender(self):
        for passenger in self.payload.passengers:
            if passenger.passengerGender not in ["M", "F"]:
                self.errors.append(
                    f"Invalid Passenger's Gender | 'M' for Male and 'F' for Female | name : {passenger.passengerName}")

    def invalid_quota(self):  # TODO
        if self.payload.quota not in ["GN", "TK", "PT", "LD", "HP", "SS"]:
            self.errors.append(
                "Invalid Quota | 'GN' for General and 'TK' for Tatkal")

    def invalid_class(self):
        if self.payload.classcode not in ["2S", "SL", "3A", "2A", "1A"]:
            self.errors.append(
                "Invalid class | '2S' for second sitting, 'SL' for sleeper, '3A' for AC 3 tier, '2A' for AC 2 tier and '1A' for AC first class")

    def invalid_date(self):
        try:
            datetime.strptime(self.payload.jrnyDate, "%Y%m%d")
        except ValueError:
            self.errors.append(
                "Invalid Journey Date | date format: 'yyyymmdd'")

    def invalid_age(self):
        for passenger in self.payload.passengers:
            if self._default_passenger_min_age > passenger.passengerAge > self._default_passenger_max_age:
                self.errors.append(
                    f"Invalid Passenger's Age | minimum valid age: 1 and maximum valid age: 125 | name: {passenger.passengerName}")

    def invalid_name(self):
        for passenger in self.payload.passengers:
            if len(passenger.passengerName) > 16:
                self.errors.append(
                    f"Invalid Passenger's Name | Max Name Legth: 16| name:{passenger.passengerName}")

            if not all(list(map(lambda x: x.isalpha(), passenger.passengerName.split(" ")))):
                self.errors.append(
                    f"Invalid Passenger's Name | Name must be Alphabetic and One Space between only| name:{passenger.passengerName}")

    def invalid_mobile(self):
        if len(self.payload.mobile) != 10 or not self.payload.mobile.isdigit():
            self.errors.append(
                f"Invalid Mobile No | No: {self.payload.mobile}")

    def invalid_paymentType(self):
        if self.payload.paymentType not in ["2", "3"]:
            self.errors.append(
                f"Invalid Payment Type| '2': Pay through Credit & Debit Cards / Net Banking / Wallets / Bharat QR / Pay on Delivery/ Rewards and Others and '3': Pay through BHIM/UPI | given {self.payload.paymentType}")
