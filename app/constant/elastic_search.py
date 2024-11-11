from enum import Enum
class CalendarInterval(str,Enum):
    DAY:str="day"
    HOUR:str='hour'
    WEEK:str='week'
    MONTH:str='month'
    QUARTER:str='quarter'
    YEAR:str='year'