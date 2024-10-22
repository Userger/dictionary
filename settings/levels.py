from modules.level import Level

self_dict_levels = (
    Level('last10', range_start=-10),
    Level('last100', range_start=-100),
    Level('all'),
)

common_levels = (
    Level('1-100',
          range_start=0,
          range_num=100,
          amount=10),
    Level('100-200',
          range_start=100,
          range_num=100,
          amount=10),
    Level('200-300',
          range_start=200,
          range_num=100,
          amount=10),
    Level('300-400',
          range_start=300,
          range_num=100,
          amount=10),
    Level('400-500',
          range_start=400,
          range_num=100,
          amount=10),
    Level('500-600',
          range_start=500,
          range_num=100,
          amount=10),
)
