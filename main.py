import asyncio
from modules.menu import Menu, ExitMenu, EscapeMenu
from modules.interface import MenuInterface
from modules.drawmenu import DrawMenu
from modules.texteditor import TextEditorMenu
from settings.levels import self_dict_levels, common_levels
from settings import SELF_DICT_DIRS

async def main():

    # PLAY MENU
    play_menu = Menu('play')

    play_common = Menu('common').add_submenu(*common_levels)
    play_self_dict = Menu('dict').add_submenu(*self_dict_levels)

    play_menu.add_submenu(play_common,
                          play_self_dict)

    # DICTIONARY MENU
    dict_menu = Menu('dict manage')
    dict_menu.add_submenu(TextEditorMenu('dict 1', SELF_DICT_DIRS))

    # EXIT MENU
    exit_menu = Menu('exit')
    exit_menu.add_submenu(ExitMenu('yes'),
                          EscapeMenu('no'))

    # SETTINGS MENU
    settings_menu = Menu('settings')
    text_editor = Menu('text editor')


    # MAIN MENU
    main_menu = Menu('main menu')
    main_menu.set_parent(exit_menu)
    main_menu.add_submenu(play_menu,
                          dict_menu,
                          settings_menu,
                          exit_menu)





    interface = MenuInterface()
    interface.add_start_menu(main_menu)

    draw_menu = DrawMenu(interface)
    await draw_menu.start()



if __name__ == '__main__':
    asyncio.run(main())
