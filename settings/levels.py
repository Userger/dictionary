from modules.level import Level, DirLevel
from modules.advancedmenu import CustomLevelMenu

def selfdict():
    return (
        Level('all'),
        Level('last10', range_start=-10),
        Level('last100', range_start=-100),
        Level('all (5min)', duration=5*60),
        Level('last50 (5min)', range_start=-100, duration=5*60),
        Level('last100 (5min)', range_start=-100, duration=5*60),
        CustomLevelMenu('custom'),
    )

def common():
    return (
        Level('1-100', range_start=0, range_num=100, amount=10),
        Level('100-200', range_start=100, range_num=100, amount=10),
        Level('200-300', range_start=200, range_num=100, amount=10),
        Level('300-400', range_start=300, range_num=100, amount=10),
        Level('400-500', range_start=400, range_num=100, amount=10),
        Level('500-600', range_start=500, range_num=100, amount=10),
    )

def categories():
   return (
       Level("all"),
       Level("all - 2 min", duration=60*2),
   )

levels = {
    "selfdict": selfdict,
    "common": common,
    "categories": categories,
}


def get_levels(name):
    if lvls := levels.get(name):
        return lvls()
    return tuple()

