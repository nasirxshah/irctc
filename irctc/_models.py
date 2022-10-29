from dataclasses import dataclass, field


# login models
@dataclass(kw_only=True)
class WebTokenModel:
    grant_type: str = field(init=False)
    username: str = field(init=False)
    password: str = field(init=False)
    captcha: str = field(init=False)
    uid: str = field(init=False)
    otpLogin: bool = field(init=False)
    nlpIdentifier: str = field(init=False)
    nlpAnswer: str = field(init=False)
    nlpToken: str = field(init=False)
    lso: str = field(init=False)
    encodedPwd: bool = field(init=False)


# booking models
@dataclass(kw_only=True)
class TrainAvlEnqModel:
    concessionBooking: bool = field(init=False)
    srcStn: str = field(init=False)
    destStn: str = field(init=False)
    jrnyClass: str = field(init=False)
    jrnyDate: str = field(init=False)
    quotaCode: str = field(init=False)
    currentBooking: str = field(init=False)
    flexiFlag: bool = field(init=False)
    handicapFlag: bool = field(init=False)
    ticketType: str = field(init=False)
    loyaltyRedemptionBooking: bool = field(init=False)
    ftBooking: bool = field(init=False)


@dataclass(kw_only=True)
class TrainFareModel:
    paymentFlag: str = field(init=False)
    concessionBooking: bool = field(init=False)
    ftBooking: bool = field(init=False)
    loyaltyRedemptionBooking: bool = field(init=False)
    ticketType: str = field(init=False)
    quotaCode: str = field(init=False)
    moreThanOneDay: bool = field(init=False)
    trainNumber: str = field(init=False)
    fromStnCode: str = field(init=False)
    toStnCode: str = field(init=False)
    isLogedinReq: bool = field(init=False)
    journeyDate: str = field(init=False)
    classCode: str = field(init=False)
    returnJourney: bool = field(init=False)
    returnTicket: bool = field(init=False)


@dataclass(kw_only=True)
class BoardingModel:
    clusterFlag: str = field(init=False)
    onwardFlag: str = field(init=False)
    cod: str = field(init=False)
    reservationMode: str = field(init=False)
    autoUpgradationSelected: bool = field(init=False)
    gnToCkOpted: bool = field(init=False)
    paymentType: int = field(init=False)
    twoPhaseAuthRequired: bool = field(init=False)
    captureAddress: int = field(init=False)
    alternateAvlInputDTO: list = field(init=False)
    passBooking: bool = field(init=False)
    journalistBooking: bool = field(init=False)
    returnJourney: bool = field(init=False)
    returnTicket: bool = field(init=False)


@dataclass(kw_only=True)
class LapFareModel:
    clusterFlag: str = field(init=False)
    onwardFlag: str = field(init=False)
    cod: str = field(init=False)
    reservationMode: str = field(init=False)
    autoUpgradationSelected: bool = field(init=False)
    gnToCkOpted: bool = field(init=False)
    paymentType: str = field(init=False)
    twoPhaseAuthRequired: bool = field(init=False)
    captureAddress: int = field(init=False)
    wsUserLogin: str = field(init=False)
    moreThanOneDay: bool = field(init=False)
    clientTransactionId: str = field(init=False)
    boardingStation: str = field(init=False)
    reservationUptoStation: str = field(init=False)
    mobileNumber: str = field(init=False)
    ticketType: str = field(init=False)
    mainJourneyTxnId: None = field(init=False)
    mainJourneyPnr: str = field(init=False)
    captcha: str = field(init=False)
    generalistChildConfirm: bool = field(init=False)
    ftBooking: bool = field(init=False)
    loyaltyRedemptionBooking: bool = field(init=False)
    nosbBooking: bool = field(init=False)
    warrentType: int = field(init=False)
    ftTnCAgree: bool = field(init=False)
    bookingChoice: int = field(init=False)
    bookingConfirmChoice: int = field(init=False)
    bookOnlyIfCnf: bool = field(init=False)
    returnJourney: bool = field(init=False)
    connectingJourney: bool = field(init=False)
    lapAvlRequestDTO: list = field(init=False)
    gstDetails: dict = field(init=False)


@dataclass(kw_only=True)
class Passenger:
    passengerName: str = field(init=False)
    passengerAge: int = field(init=False)
    passengerGender: str = field(init=False)
    passengerSerialNumber: int = field(init=False)
    passengerBerthChoice: str = ""
    passengerFoodChoice: None = None
    passengerBedrollChoice: None = None
    passengerNationality: str = "IN"
    passengerCardTypeMaster: None = None
    passengerCardNumberMaster: None = None
    psgnConcType: None = None
    psgnConcCardId: None = None
    psgnConcDOB: None = None
    psgnConcCardExpiryDate: None = None
    psgnConcDOBP: None = None
    softMemberId: None = None
    softMemberFlag: None = None
    psgnConcCardExpiryDateP: None = None
    passengerVerified: bool = False
    masterPsgnId: None = None
    mpMemberFlag: None = None
    passengerForceNumber: None = None
    passConcessionType: str = "0"
    passUPN: None = None
    passBookingCode: None = None
    childBerthFlag: bool = True
    passengerCardType: str = "NULL_IDCARD"
    passengerIcardFlag: bool = False
    passengerCardNumber: None = None


@dataclass(kw_only=True)
class LapDTO:
    trainNo: str = field(init=False)
    journeyDate: str = field(init=False)
    fromStation: str = field(init=False)
    toStation: str = field(init=False)
    journeyClass: str = field(init=False)
    quota: str = field(init=False)
    coachId: None = field(init=False)
    reservationChoice: str = field(init=False)
    ignoreChoiceIfWl: bool = field(init=False)
    travelInsuranceOpted: bool = field(init=False)
    warrentType: int = field(init=False)
    coachPreferred: bool = field(init=False)
    autoUpgradation: bool = field(init=False)
    bookOnlyIfCnf: bool = field(init=False)
    addMealInput: None = field(init=False)
    concessionBooking: bool = field(init=False)
    passengerList: list = field(init=False)
    ssQuotaSplitCoach: str = field(init=False)


@dataclass(kw_only=True)
class AltDTO:
    trainNo: str = field(init=False)
    destStn: str = field(init=False)
    srcStn: str = field(init=False)
    jrnyDate: str = field(init=False)
    quotaCode: str = field(init=False)
    jrnyClass: str = field(init=False)


# captcha models

@dataclass(kw_only=True)
class NlpOptions:
    key: str = field(init=False)
    ajax: int = field(init=False)
    ajaxContainer: str = field(init=False)
    html5audio: str = field(init=False)
    t: str = field(init=False)
    token: str = field(init=False)
    mandatorytype: str = field(init=False)
    nlpRefCnt: str = field(init=False)
    theme_size: str = field(init=False)


@dataclass(kw_only=True)
class BookingNlpOptions(NlpOptions):
    irctc_class_code: str = field(init=False)
    irctc_arrival_date: str = field(init=False)
    irctc_journey_date: str = field(init=False)
    irctc_from_station_code: str = field(init=False)
    irctc_quota: str = field(init=False)
    irctc_to_station: str = field(init=False)
    irctc_train_type: str = field(init=False)
    irctc_age: int = field(init=False)
    irctc_gender: int = field(init=False)
