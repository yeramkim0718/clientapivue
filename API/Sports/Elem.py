from enum import IntEnum,Enum

class Sport(IntEnum) :
    id = 0
    logo = 1
    bg_img = 2

class League(IntEnum) :
    id = 0
    logo = 1
    sport_id = 2

class Team(IntEnum) :
    id = 0
    logo = 1
    league_id = 2

class Lang(IntEnum) :
    ko_KR = 3
    ja_JP = 4
    fr_FR = 5
    es_ES = 6
    en_US = 7
    en_GB = 8
    de_DE = 9
    nl_NL = 10     
    
