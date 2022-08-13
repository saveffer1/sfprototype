import pygame as pg
import pygame_menu
from pygame_menu import sound
import game
import configparser

# Load configuration
player_config = configparser.ConfigParser()
player_config.read('resource/data/game_data.ini')
game_config = configparser.ConfigParser()
game_config.read('resource/data/game_setting.ini')

# Initialize pygame
pg.init()
# Create the menu at 800x600 resolution
surface = pg.display.set_mode((1200, 600))
pg.display.set_caption(game_config.get('config', 'game_name'))
background_image = pygame_menu.BaseImage(image_path='resource/images/menu_bg.jpg')
menu = pygame_menu.Menu(game_config.get('config', 'game_name'), 600, 400, theme=pygame_menu.themes.THEME_DARK) #Create the menu

""" sound setup"""
sound_engine = sound.Sound()
#sound_engine.set_sound(sound.SOUND_TYPE_CLICK_MOUSE, 'resource/sound/click_error.wav')
#sound_engine.set_sound(sound.SOUND_TYPE_OPEN_MENU, 'resource/sound/select_click.wav')
#sound_engine.set_sound(sound.SOUND_TYPE_CLOSE_MENU,'resource/sound/select_click.wav')
#sound_engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION,'resource/sound/single_press.wav')
#sound_engine.set_sound(sound.SOUND_TYPE_KEY_DELETION, 'resource/sound/backspace.wav')
#sound_engine.set_sound(sound.SOUND_TYPE_ERROR, 'resource/sound/select_click.wav')
#sound_engine.set_sound(sound.SOUND_TYPE_EVENT, 'resource/sound/click_error.wav')
#sound_engine.set_sound(sound.SOUND_TYPE_EVENT_ERROR, 'resource/sound/click_error.wav')
#sound_engine.set_sound(sound.SOUND_TYPE_WIDGET_SELECTION, 'resource/sound/click_error.wav')
"""end sound setup"""

# draw background
def main_background() -> None:
    background_image.draw(surface)
    
# Save config of ini file
def save_config(config, file):
    # save player config
    if config == 'player':
        with open(file, 'w') as configfile:
            player_config.write(configfile)
    # save game config
    elif config == 'game': 
        with open(file, 'w') as configfile:
            game_config.write(configfile)

# Set up the sound (on, off)
def sound_setting(value, sound):
    game_config.set('sound', 'sound_config', str(sound)) # set config file
    save_config('game', 'resource/data/game_setting.ini') # save config file

# Set up the last played player
def last_played_player(value):
    player_config.set('player', 'latest_player', str(value)) # set config file
    save_config('player', 'resource/data/game_data.ini') # save set config file

# Start the game function
def start_the_game():
    global menu
    pg.mouse.set_cursor((8, 8), (0, 0), (0, 0, 0, 0, 0, 0, 0, 0),(0, 0, 0, 0, 0, 0, 0, 0))  # visible cursor
    clock = pg.time.Clock()
    all_sprites = pg.sprite.Group()
    entity = game.Entity((100, 300), all_sprites)
    paused = False
    score = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    paused = not paused
        
        if not paused:
            all_sprites.update()
            score += 1 # increase score
            # keep high score condition
            if score > player_config.getint('score', 'highest_score'): # if score is higher than highest score
                player_config.set('score', 'highest_score', str(score)) # set highest score
                player_config.set('score', 'player_name', str(player_config.get('player', 'latest_player'))) # set player name
                save_config('player', 'resource/data/game_data.ini') # save set config file
            surface.fill((30, 30, 30))
            all_sprites.draw(surface)

            pg.display.flip()
            clock.tick(120)
        else:
            """ Pause menu section"""
            pause_menu = pygame_menu.Menu(game_config.get('config', 'game_name'), 600, 400, theme=pygame_menu.themes.THEME_DARK)  # Create the paused menu
            pause_menu.set_sound(sound_engine, recursive=True) # set sound
            pause_menu.add.label('Score : ' + str(score)) # add score label
            pause_menu.add.button("Resume") # add resume button
            pause_menu.add.button("Play again", start_the_game) # add play again button
            pause_menu.add.button("Settings", setting_menu) # add setting button
            #pause_menu.add.button('Quit to menu', menu)  # back to main menu
            pause_menu.add.button('Quit', pygame_menu.events.EXIT) # exit game
            pause_menu.mainloop(surface, main_background) # draw the pause menu
            """END Pause menu section"""
            

""" Setting menu section"""
# Create the setting menu
setting_menu = pygame_menu.Menu(
    height=400,
    theme=pygame_menu.themes.THEME_DARK,
    title='Settings',
    width=600
)
# Add the sound setting
setting_menu.add.selector('Sound :', [('Off', 0), ('On', 1)], default=int(
    game_config.get('sound', 'sound_config')), onchange=sound_setting)
"""END Setting menu section"""

""" About menu section"""
# Create the about menu
about_menu = pygame_menu.Menu(
    height=400,
    theme=pygame_menu.themes.THEME_DARK,
    title='About this game',
    width=600
)
# about text
# read about text from config file
get_about_text = game_config.get('config', 'about_text')
get_about_text = get_about_text.split(',')  # split the text into list
about_text = "\n".join(get_about_text)  # join the list into string
about_menu.add.label(about_text)  # add the text to the menu
"""END About menu section"""
""" Main menu section"""
menu.set_sound(sound_engine, recursive=True) # set sound

menu.add.label('High score : ' + player_config.get('score','player_name') + ' | ' + player_config.get('score', 'highest_score') + ' points') # add high score label
menu.add.text_input('Name : ', default=player_config.get('player', 'latest_player'), onchange=last_played_player) # add player name input box
menu.add.button("Play", start_the_game) # add play button
menu.add.button("Settings", setting_menu) # add setting button
menu.add.button("About", about_menu) # add about button
menu.add.button('Quit to desktop', pygame_menu.events.EXIT) # add quit button

menu.mainloop(surface, main_background) # run the main menu
"""END Main menu section"""