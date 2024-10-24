import asyncio
from modules.menu import Menu, ExitMenu, EscapeMenu
from modules.advancedmenu import NewTextEditorMenu, TextEditorMenu
from modules.interface import MenuInterface
from modules.drawmenu import DrawMenu
from settings.levels import self_dict_levels, common_levels, category_levels
from settings import SELF_DICT_DIRS

async def main():

    # PLAY MENU
    play_menu = Menu('play')

    play_common = Menu('common').add_submenu(*common_levels)
    play_self_dict = Menu('dict').add_submenu(*self_dict_levels)
    play_category = Menu('categories').add_submenu(*category_levels)

    play_menu.add_submenu(play_common,
                          play_self_dict,
                          play_category)

    # DICTIONARY MENU
    dict_menu = Menu('dict manage')
    dict_menu.add_submenu(TextEditorMenu('self dict 1', SELF_DICT_DIRS[0]),
                          TextEditorMenu('animals', 'dicts/categories/animals'))

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
