import asyncio
from modules.menu import Menu, ExitMenu, EscapeMenu
from modules.level import Level
from modules.interface import MenuInterface
from modules.drawmenu import DrawMenu
from modules.dictmanage import DictManage

async def main():

    # PLAY MENU
    play_menu = Menu('play')
    play_common = Menu('common')
    play_common.add_submenu(Level('test',
                                  duration=10),
                            Level('test2',
                                  duration=30),
                            Level('200-250',
                                  duration=25,
                                  amount=5,
                                  range_start=200,
                                  range_num=50),
                            Level('last-10',
                                  range_start=-10,
                                  range_num=None),
                            Level('1001-1100',
                                  range_start=1001,
                                  range_num=100),
                            Level('1-10',
                                  range_start=1,
                                  amount=10,
                                  range_num=10,
                                  duration=5*60))
    play_self_dict = Menu('dict')
    play_self_dict.add_submenu(
                               Level('last10', range_start=-10),
                               Level('last100', range_start=-100),
                               Level('all'),
                               Level('test', range_num=1, amount=1),
                               Level('test2', range_start=2, amount=10),
                               )
    play_menu.add_submenu(play_common,
                          play_self_dict)

    # DICTIONARY MENU
    dict_menu = Menu('dict manage')
    dict_menu.add_submenu(DictManage('dict 1'))

    # EXIT MENU
    exit_menu = Menu('exit')
    exit_menu.add_submenu(ExitMenu('yes'),
                          EscapeMenu('no'))

    # MAIN MENU
    main_menu = Menu('main menu')
    main_menu.set_parent(exit_menu)
    main_menu.add_submenu(play_menu,
                          dict_menu,
                          exit_menu)

    interface = MenuInterface()
    interface.add_start_menu(main_menu)

    draw_menu = DrawMenu(interface)
    await draw_menu.start()



if __name__ == '__main__':
    asyncio.run(main())
