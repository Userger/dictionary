import asyncio
from modules.menu import Menu, ExitMenu, EscapeMenu
from modules.advancedmenu import NewTextEditorMenu, TextEditorMenu
from modules.interface import MenuInterface
from modules.drawmenu import DrawMenu
from settings.levels import get_levels
from settings import DICT_DIR

from os import listdir
from pathlib import Path
from copy import deepcopy


async def main():
    # PLAY MENU
    play_menu = Menu('play')

    dicts_path = Path(DICT_DIR)
    for directory_name in listdir(dicts_path):
        mode_menu = Menu(directory_name)
        for dct in listdir(dicts_path / directory_name):
            mode_submenu = Menu(dct)
            mode_submenu_levels = get_levels(directory_name)
            mode_submenu.add_submenu(*mode_submenu_levels)
            mode_menu.add_submenu(mode_submenu)

        play_menu.add_submenu(mode_menu)


    # DICTIONARY MENU
    dict_menu = Menu('dict manage')
    dict_submenu = [
            TextEditorMenu(f'edit {name}', str(Path(DICT_DIR) / "selfdict" / name))
            for name in listdir(dicts_path / "selfdict")
    ]
    dict_menu.add_submenu(*dict_submenu)

    # EXIT MENU
    exit_menu = Menu('exit')
    exit_menu.add_submenu(ExitMenu('yes'),
                          EscapeMenu('no'))

    # SETTINGS MENU
    settings_menu = Menu('settings')
    text_editor = Menu('text editor')
    text_editor.add_submenu(NewTextEditorMenu('change'))
    settings_menu.add_submenu(text_editor)

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
