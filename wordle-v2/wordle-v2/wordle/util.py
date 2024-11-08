import pygame_menu
from .colors import GREEN
def find_center(width:int, height:int):
	return width/2, height/2

main_theme_style = {
    "background_color": (200, 200, 200),
    "border_color": (128, 128, 128),
    "border_width": 5,
    #"cursor_color": (int(), int(), int()),
    "fps": 60,
    #"readonly_color": (int(), int(), int()),
    "title": True,
    "title_background_color": GREEN,
    "title_close_button": True,
    "title_fixed": True,
    #"title_floating": True,
    #"title_font": pygame.font.SysFont(None, 55),
    "title_font_antialias": True,
    "title_font_color": (int(), int(), int()),
    "title_font_size": 35,
    #"widget_font": pygame.font,
    "widget_font_color": (0,0,0),
    "widget_font_size": 35
}

def get_theme():
	return pygame_menu.Theme(**main_theme_style)