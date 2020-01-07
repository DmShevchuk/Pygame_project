import pygame
import random
import os, sys

pygame.init()
SIZE = [600, 400]
screen = pygame.display.set_mode(SIZE)
BLACK = pygame.Color('black')

bullets_sound = pygame.mixer.Sound('data/bullet.wav')
monster_roar_sound = pygame.mixer.Sound('data/dragons_roar.wav')
monster_hero_boom_sound = pygame.mixer.Sound('data/boom.wav')

screen.fill(BLACK)

hero_group = pygame.sprite.Group()
levels_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
birds_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()
monsters_group = pygame.sprite.Group()
health_monsters_group = pygame.sprite.Group()


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


def start_screen():
    fon = pygame.transform.scale(load_image('fon2.jpg'), (SIZE[0], SIZE[1]))
    screen.blit(fon, (0, 0))
    title = ['', 'T', 'h', 'e', 'b', 'e', 's', 't', 'g', 'a', 'm', 'e']
    shoot = True
    bullet_update = True
    FPS = 60
    index = 0
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return
        if hero.rect.x < SIZE[0] // 3:
            hero.rect.x += 2
            hero.cur_frame = (hero.cur_frame + 1) % len(hero.frames)
            hero.image = hero.frames[hero.cur_frame]
            hero.mask = pygame.mask.from_surface(hero.image)
        elif shoot:
            Bullet(hero.rect.x, hero.rect.y, 'bullet2.png')
            shoot = False
        if bullet_update:
            for elem in bullets_group:
                elem.update(x=10, y=-10)
                if elem.rect.y < SIZE[1] // 3:
                    elem.kill()
                    fon = pygame.transform.scale(load_image('fon3.jpg'), (SIZE[0], SIZE[1]))
                    screen.blit(fon, (0, 0))
                    Bird(load_image('bird1.png'), 5, 1, 500, SIZE[1] // 4)
                    FPS = 30
                    bullet_update = False
        else:
            for bird in birds_group:
                bird.update()
            create_particles((bird.rect.x + 50, bird.rect.y))
            index += 1
            text_coord = bird.rect.x + 50
            font = pygame.font.Font(None, 50)
            for line in title[:index]:
                string_rendered = font.render(line, 1, pygame.Color('blue'))
                intro_rect = string_rendered.get_rect()
                text_coord += 10
                intro_rect.left = text_coord
                intro_rect.y = bird.rect.y
                text_coord += intro_rect.height
                screen.blit(string_rendered, intro_rect)
        hero_group.draw(screen)
        bullets_group.draw(screen)
        birds_group.draw(screen)
        stars_group.draw(screen)
        stars_group.update()
        pygame.display.flip()
        screen.blit(fon, (0, 0))
        pygame.time.Clock().tick(FPS)
        clock.tick(FPS)


def create_particles(position):
    particle_count = 3
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers))


class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, health=5):
        super().__init__(hero_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.health = health
        self.collide_with_monster_counter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self, x, y, check_collide=True):
        level.rect.x -= x
        level.rect.y -= y
        if not pygame.sprite.collide_mask(self, level) or not check_collide:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
            self.mask = pygame.mask.from_surface(self.image)
            dragon.rect.x -= x
            dragon_health.update(dragon)
        else:
            level.rect.x += x
            level.rect.y += y
        if len(monsters_group) > 0 and pygame.sprite.collide_mask(self, dragon):
            self.health -= 1
            monster_hero_boom_sound.play()
            # Если игрок подходит слева к монстру, то его нужно отбросить ближе к старту уровня. Если справа, то дальше от старта.
            if hero_direction == 'right':
                level.rect.x -= 100
                dragon.rect.x += 100
            else:
                level.rect.x += 100
                dragon.rect.x -= 100
            dragon_health.update(dragon)
            if self.health < 0:
                global hero, hero_group
                self.kill()
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero.png"), 6, 1, 30, start_y)
                level.rect.x = 0
                dragon.rect.x = 400
                dragon.rect.y = 270
                dragon.health = 5
                dragon_health.update(dragon)


class Level(pygame.sprite.Sprite):
    levels_image = {'first': load_image('level1.png')}

    def __init__(self, level):
        super().__init__(levels_group)
        self.image = Level.levels_image[level]
        self.rect = self.image.get_rect()
        self.rect.bottom = SIZE[1]
        self.mask = pygame.mask.from_surface(self.image)


class Monster(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(monsters_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.health = 5

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Health_monster(pygame.sprite.Sprite):
    def __init__(self, monster):
        super().__init__(health_monsters_group)
        self.image = pygame.Surface([52, 10])
        pygame.draw.rect(self.image, (255, 255, 255), (0, 0, 52, 10), 1)
        pygame.draw.rect(self.image, pygame.color.Color('green'), (1, 1, 50, 8), 0)
        self.rect = self.image.get_rect()
        self.rect.x = monster.rect.x + 18
        self.rect.y = monster.rect.y - 10
        self.heatlh = monster.health

    def update(self, monster):
        self.rect.x = monster.rect.x + 18
        self.rect.y = monster.rect.y - 10
        pygame.draw.rect(self.image, pygame.color.Color('black'), (1, 1, 50, 8), 0)
        pygame.draw.rect(self.image, pygame.color.Color('green'), (1, 1, monster.health * 10, 8), 0)


class Bullet(pygame.sprite.Sprite):
    screen_rect = (0, 0, SIZE[0], SIZE[1])

    def __init__(self, x, y, image):
        super().__init__(bullets_group)
        self.image = load_image(image, color_key=-1)
        self.rect = self.image.get_rect()
        self.direction = hero_direction
        if self.direction == 'right':
            self.rect.x = x + (hero.rect.width // 4) * 3
        else:
            self.rect.x = x
            self.image = pygame.transform.flip(self.image, True, False)
        self.rect.y = y + hero.rect.height // 3

    def update(self, x=15, y=0):
        if self.direction == 'right':
            self.rect.x += x
        else:
            self.rect.x -= x
        self.rect.y += y
        if not self.rect.colliderect(Bullet.screen_rect):
            self.kill()
        if len(monsters_group) > 0 and pygame.sprite.collide_mask(self, dragon):
            self.kill()
            monster_roar_sound.play()
            dragon.health -= 1
            dragon_health.update(dragon)
            if dragon.health == 0:
                dragon.kill()
                dragon_health.kill()


class Bird(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(birds_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.health = 5

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.rect.x -= 5
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        self.mask = pygame.mask.from_surface(self.image)
        if not self.rect.colliderect((50, 0, SIZE[0], SIZE[1])):
            self.kill()


class Particle(pygame.sprite.Sprite):
    fire = [load_image("star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(stars_group)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos
        self.gravity = 0.25

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect((0, 0, SIZE[0], SIZE[1])):
            self.kill()


level = Level('first')
hero = Hero(load_image("hero.png"), 6, 1, 100, 300)
dragon = Monster(load_image("dragon.png"), 8, 2, 400, 270)
dragon_health = Health_monster(dragon)
health_image = load_image('health.png', color_key=-1)
boom_image = load_image('boom.png', color_key=-1)
start_y = level.rect.y - level.rect.height - 15
clock = pygame.time.Clock()
FPS = 50
running = True
start_screen_show = True
x, y = 0, 0
dy = 0
hero_direction = 'right'
# Даёт игроку возможность перепрыгнуть через монстра
previous_button = None
hero_health = hero.health

background_image = load_image('country_field.png')

while running:
    if start_screen_show:
        start_screen()
        start_screen_show = False
        hero_group = pygame.sprite.Group()
        hero = Hero(load_image("hero.png"), 6, 1, 100, start_y)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_RIGHT]:
                hero_direction = 'right'
                x, y = (20, 0)
                x_d, y_d = hero.rect.x, hero.rect.y
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero.png"), 6, 1, x_d, y_d, health=hero.health)
            if pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_LEFT]:
                hero_direction = 'left'
                x, y = (-20, 0)
                x_d, y_d = hero.rect.x, hero.rect.y
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero_left.png"), 6, 1, x_d, y_d, health=hero.health)
            if event.key == pygame.K_RIGHT:
                hero_direction = 'right'
                x, y = (10, 0)
                x_d, y_d = hero.rect.x, hero.rect.y
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero.png"), 6, 1, x_d, y_d, health=hero.health)
            if event.key == pygame.K_LEFT:
                hero_direction = 'left'
                x_d, y_d = hero.rect.x, hero.rect.y
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero_left.png"), 6, 1, x_d, y_d, health=hero.health)
                x, y = (-10, 0)
            if event.key == pygame.K_UP:
                if dy != 5:
                    hero.rect.y -= 100
                    dy = 5
                previous_button = 1
            if event.key == pygame.K_SPACE:
                bullets_sound.play()
                Bullet(hero.rect.x, hero.rect.y, 'bullet.png')
                previous_button = 0
            # Перезагрузка уровня при нажатии Ctrl + R
            if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_r]:
                hero.kill()
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero.png"), 6, 1, 30, start_y)
                hero_direction = 'right'
                level.rect.x = 0
                dragon = Monster(load_image("dragon.png"), 8, 2, 400, 270)
                dragon_health = Health_monster(dragon)
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                x, y = 0, 0

    if x != 0:
        hero.update(x, y)

    # Если герой в воздухе, то его нужно возвращать на землю
    if dy != 0:
        if start_y > hero.rect.y:
            hero.rect.y += dy
        else:
            dy = 0

    screen.fill(BLACK)
    screen.blit(background_image, (0, 0))
    for i in range(hero.health):
        screen.blit(health_image, (420 + i * 35, 10))

    # Если xp героя меньше, чем на предудущем шаге
    if hero_health != hero.health:
        screen.blit(boom_image, (dragon.rect.x - 50, dragon.rect.y - 50))
        hero_health = hero.health
    hero_group.draw(screen)
    levels_group.draw(screen)
    bullets_group.draw(screen)
    health_monsters_group.draw(screen)
    monsters_group.draw(screen)
    bullets_group.update()
    monsters_group.update()
    clock.tick(FPS)
    pygame.display.flip()