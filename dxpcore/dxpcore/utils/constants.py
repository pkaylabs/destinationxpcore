from enum import Enum


class HotelCategory(Enum):
    '''App category enumeration for Hotels.'''
    STANDARD = 'Standard'
    SHORTSTAY = 'Short Stay'
    FAMILY = 'Family'
    BOOTIQUE = 'Bootique'


class PoliticalCategory(Enum):
    '''App category enumeration for Political.'''
    MINISTRY = 'Ministry'
    DEPARTMENT = 'Department'
    AGENCY = 'Agency'
    OTHERS = 'Others'


class TourismCategory(Enum):
    '''App category enumeration for Tourism.'''
    HISTORICAL = 'Historical'
    CULTURAL = 'Cultural'
    LEISURE = 'Leisure'
    NATURE = 'Nature'
    ENTERTAINMENT = 'Entertainment'
    OTHERS = 'Others'

class BlogCategory(Enum):
    '''Type enumeration for Blog model'''
    TRAVEL = "TRAVEL BLOG"
    FUNFACT = "FUN FACT"
    OTHER = "OTHER BLOG"