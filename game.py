import pygame as pg
from pygame.math import Vector2
import pygame_menu

class Entity(pg.sprite.Sprite):

    def __init__(self, pos, *groups):
        super().__init__(*groups)
        self.image = pg.Surface((30, 30))
        self.image.fill(pg.Color('dodgerblue1'))
        self.rect = self.image.get_rect(center=pos)
        self.pos = Vector2(pos)

    def update(self):
        # Get a vector that points from the position to the target.
        heading = pg.mouse.get_pos() - self.pos
        self.pos += heading * 0.1  # Scale the vector to the desired length.
        self.rect.center = self.pos

# Initialize pygame and run this if user run this file
def main():
    print('Error! please run main.py')
    pg.init()
    surface = pg.display.set_mode((600, 400))
    pg.display.set_caption('Error!')
    menu = pygame_menu.Menu('Error!', 600, 400, theme=pygame_menu.themes.THEME_DARK)
    menu.add.label("Please run main.py")
    menu.add.button('OK', pygame_menu.events.EXIT)
    menu.mainloop(surface)

if __name__ == '__main__':
    main()