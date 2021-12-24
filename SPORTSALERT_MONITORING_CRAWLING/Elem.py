from enum import IntEnum,Enum

class SportsElem(Enum) :
    BASEBALL = 'BASEBALL'
    FOOTBALL = 'FOOTBALL'
    AMERICANFOOTBALL = 'AMERICAN FOOTBALL'
    BASKETBALL = 'BASKETBALL'
    ICEHOCKEY = 'ICEHOCKEY'
    CRICKET = 'CRICKET'

class PushElem(IntEnum) :
    ID = 0
    START_TIME = 1
    LEAGUE = 2
    SPORT_ID = 3
    HOME = 4
    AWAY = 5
    LOG_TIME = 6
    STATUS = 7
    STATE = 8
    SCORES = 9
    CHECKING = 10
    TOTALERRNUM = 11
    ERRORTYPE = 12

class CRAWLEINFO(IntEnum) :
    URL = 0
    TOTALTAG = 1
    SCORETAG = 2
    PUSHTAG = 3

class WEBElem(IntEnum) :
    WEBID = 0
    TIME = 1
    HOME = 2
    AWAY = 3
    HOME_SCORE = 4
    AWAY_SCORE = 5
    PUSH = 6

class BASEBALLPUSH(IntEnum) :
    HOME1 = 0
    AWAY1 = 1
    HOME2 = 2
    AWAY2 = 3
    HOME3 = 4
    AWAY3 = 5
    HOME4 = 6
    AWAY4 = 7
    HOME5 = 8
    AWAY5 = 9
    HOME6 = 10
    AWAY6 = 11
    HOME7 = 12
    AWAY7 = 13
    HOME8 = 14
    AWAY8 = 15
    HOME9 = 16
    AWAY9 = 17    
    HOME_OVERTIME = 18
    AWAY_OVERTIME = 19

class FOOTBALLPUSH(IntEnum) :
    HALFSCORES = 0
    OVERSCORES = 1

class BASKETBALLPUSH(IntEnum) :
    HOME1 = 0
    AWAY1 = 1
    HOME2 = 2
    AWAY2 = 3    
    HOME3 = 4
    AWAY3 = 5    
    HOME4 = 6
    AWAY4 = 7    
    HOME_OVERTIME = 8
    AWAY_OVERTIME = 9

class ICEHOCKEYPUSH(IntEnum) :
    HOME1 = 0
    AWAY1 = 1
    HOME2 = 1
    AWAY2 = 5
    HOME3 = 2
    AWAY3 = 6
    HOME_OVERTIME = 3
    AWAY_OVERTIME = 7

class AMERICANPUSH(IntEnum) :
    HOME1 = 0
    AWAY1 = 1
    HOME2 = 2
    AWAY2 = 3
    HOME3 = 4
    AWAY3 = 5
    HOME4 = 6
    AWAY4 = 7
    HOME_OVERTIME = 8
    AWAY_OVERTIME = 9

