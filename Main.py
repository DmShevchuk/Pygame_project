import pygame
import os


pygame.init()
SIZE = [600, 400]
screen = pygame.display.set_mode(SIZE)
BLACK = pygame.Color('black')
screen.fill(BLACK)

def load_image(name, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Can`t load image with name', name)
        raise SystemExit(message)

    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
    else:
        image = image.convert_alpha()
    return image




hero_group = pygame.sprite.Group()
levels_group = pygame.sprite.Group()

class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(hero_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, x, y):
        self.rect.x += x
        self.rect.y += y
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        #!!!!!!!!!!!!!!!!!!!!!!!!!!!
        if y < 0:
            self.image = pygame.transform.flip(self.frames[self.cur_frame], 1, 0)
        else:
            self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)


class Level(pygame.sprite.Sprite):
    levels_image = {'first': load_image('level.jpg')}

    def __init__(self, level):
        super().__init__(levels_group)
        self.image = Level.levels_image[level]
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect.bottom = SIZE[1]


level = Level('first')
start_y = level.rect.y - level.rect.height - 10
hero = Hero(load_image("hero.png"), 6, 1, 30, start_y)

clock = pygame.time.Clock()
FPS = 50
running = True
x, y = 0, 0

dy = 0

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                    x, y = 5, 0
            if event.key == pygame.K_LEFT:
                if dy == 5:
                    x, y = -3, 0
                else:
                    x, y = -5, 0
            if event.key == pygame.K_UP:
                if dy != 5:
                    hero.update(0, -100)
                    dy = 5
        if event.type == pygame.KEYUP:
            if event.key in(pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                x, y = 0, 0

    if x != 0 and y ==0:
        hero.update(x, y)
    if dy != 0:
        if start_y > hero.rect.y:
            hero.update(x, dy)
        else:
            dy = 0
    screen.fill(BLACK)
    hero_group.draw(screen)
    levels_group.draw(screen)
    clock.tick(FPS)
    pygame.display.flip()

