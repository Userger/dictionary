import os
from .menu import Menu
from settings import SELF_DICT_DIRS
class DictManage(Menu):
    async def run(self):
        os.system(f'vim {SELF_DICT_DIRS[0]}')
