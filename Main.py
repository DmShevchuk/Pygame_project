import pygame
import random
import os, sys

pygame.init()
SIZE = [600, 400]

# основное окно
screen = pygame.display.set_mode(SIZE)
BLACK = pygame.Color('black')

# Звуки
bullets_sound = pygame.mixer.Sound('data/bullet.wav')
monster_roar_sound = pygame.mixer.Sound('data/dragons_roar.wav')
monster_hero_boom_sound = pygame.mixer.Sound('data/boom.wav')

screen.fill(BLACK)

# Инициализация групп спрайтов
hero_group = pygame.sprite.Group()
levels_group = pygame.sprite.Group()
bullets_group = pygame.sprite.Group()
birds_group = pygame.sprite.Group()
stars_group = pygame.sprite.Group()
monsters_group = pygame.sprite.Group()
health_monsters_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
islands_group = pygame.sprite.Group()


# Загрузка всех изображений для отражения на экране
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


class Hero_traning(pygame.sprite.Sprite):
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

    def update(self, x, y):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]
        if self.rect.x > 320:
            self.rect.x -= 15
        if self.rect.x < 10:
            self.rect.x += 15
        self.rect.x += x
        self.rect.y += y


class Hero(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y, health=5, score=0):
        super().__init__(hero_group)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.health = health
        self.score = score
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
            for coin in coin_group:
                coin.rect.x -= x
            for island in islands_group:
                island.rect.x -= x
        else:
            level.rect.x += x
            level.rect.y += y
        if len(monsters_group) > 0 and pygame.sprite.collide_mask(self, dragon):
            self.health -= 1
            monster_hero_boom_sound.play()
            # Если игрок подходит слева к монстру, то его нужно отбросить ближе к старту уровня.
            # Если справа, то дальше от старта.
            if hero_direction == 'right':
                level.rect.x -= 100
                dragon.rect.x += 100
                for coin in coin_group:
                    coin.rect.x += 100

                for island in islands_group:
                    island.rect.x += 100
            else:
                level.rect.x -= 100
                dragon.rect.x -= 100
                for coin in coin_group:
                    coin.rect.x -= 100

                for island in islands_group:
                    island.rect.x -= 100

            dragon_health.update(dragon)

            if self.health < 0:
                restart()
                # global hero_group, hero
                # self.kill()
                # hero_group = pygame.sprite.Group()
                # hero = Hero(load_image("hero.png"), 6, 1, 30, start_y)
                # level.rect.x = 0
                # dragon.rect.x = 400
                # dragon.rect.y = 270
                # dragon.health = 5
                # dragon_health.update(dragon)
                #
                # for coin in coin_group:
                #     coin.kill()
                #
                # for island in islands_group:
                #     island.kill()
                #
                # for i in range(len(coin_coords)):
                #     Money(load_image('coin.png'), 6, 1, coin_coords[i][0], coin_coords[i][1])
                #
                # for i in range(len(island_coords)):
                #     Island(island_coords[i][0], island_coords[i][1], island_coords[i][2])

        for coin in coin_group:
            if pygame.sprite.collide_mask(self, coin):
                self.score += 20
                coin.kill()


class Level(pygame.sprite.Sprite):
    levels_image = {'first': load_image('level1.png')}

    def __init__(self, level):
        super().__init__(levels_group)
        self.image = Level.levels_image[level]
        self.rect = self.image.get_rect()
        self.rect.bottom = SIZE[1]
        self.mask = pygame.mask.from_surface(self.image)


class Island(pygame.sprite.Sprite):
    level_image = {'classic_island': load_image('classic_island.png')}

    def __init__(self, type, x, y):
        super().__init__(islands_group)
        self.image = Island.level_image[type]
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y
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


class Money(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(coin_group)
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
                hero.score += 50

        if pygame.sprite.spritecollide(self, islands_group, False):
            self.kill()


def training():
    WHITE = (255, 255, 255)
    # этап №1 прыжок
    hero_traning = Hero_traning(load_image("hero.png"), 6, 1, 100, start_y)
    level_traning = Level('first')
    training_sprite = pygame.sprite.Group()
    wizard = pygame.sprite.Sprite()
    wizard_image = load_image("Волшебник.png")
    wizard = pygame.sprite.Sprite()
    wizard.image = wizard_image
    wizard.rect = wizard.image.get_rect()
    training_sprite.add(hero_traning)
    dy_traning = 0
    training_sprite.add(level_traning)
    training_sprite.add(wizard)
    wizard.rect.topleft = 420, start_y - 5
    training_sprite.add(wizard)
    font = pygame.font.Font(None, 20)
    text = font.render('Приветствую тебя, странник.', 1, (255, 255, 255))
    text2 = font.render('Я - волшебник Мерлин', 1, (255, 255, 255))
    text3 = font.render('Помогу тебе выжить в этом мире.', 1, (255, 255, 255))
    text4 = font.render('Для начала подпрыгни,', 1, (255, 255, 255))
    text5 = font.render('Используй стрелочку вверх.', 1, (255, 255, 255))
    run = True
    jump = False
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hero_traning.kill()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    jump = True
                    if dy_traning != 5:
                        hero_traning.rect.y -= 100
                        dy_traning = 5
        if dy_traning != 0:
            if start_y > hero_traning.rect.y:
                hero_traning.rect.y += dy_traning
            else:
                dy_traning = 0
                if jump:
                    run = False
        screen.fill(BLACK)
        training_sprite.draw(screen)
        screen.blit(text, (360, 180))
        screen.blit(text2, (380, 195))
        screen.blit(text3, (350, 210))
        screen.blit(text4, (370, 225))
        screen.blit(text5, (355, 240))
        clock.tick(FPS)
        pygame.display.flip()
    # этап №2 движения влево и вправо
    run = True
    text = font.render('Молодец!', 1, WHITE)
    text2 = font.render('А теперь собери монетки,', 1, WHITE)
    text3 = font.render('Используя стрелочки влево и вправо.', 1, WHITE)
    coin_traning = Money(load_image("coin.png"), 6, 1, 300, level_traning.rect.y - 30)
    coin1 = True
    coin2 = False
    training_sprite.add(coin_traning)
    hero_direction_training = 'right'
    x, y = 0, 0
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                hero_traning.kill()
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    hero_direction_training = 'right'
                    x, y = (10, 0)
                    x_d, y_d = hero_traning.rect.x, hero_traning.rect.y
                    hero_traning.kill()
                    hero_traning = Hero_traning(load_image("hero.png"), 6, 1, x_d, y_d, health=hero_traning.health)
                    training_sprite.add(hero_traning)
                if event.key == pygame.K_LEFT:
                    hero_direction_training = 'left'
                    x_d, y_d = hero_traning.rect.x, hero_traning.rect.y
                    hero_traning.kill()
                    hero_traning = Hero_traning(load_image("hero_left.png"), 6, 1, x_d, y_d, health=hero_traning.health)
                    training_sprite.add(hero_traning)
                    x, y = (-10, 0)
                if event.key == pygame.K_UP:
                    if dy_traning != 5:
                        hero_traning.rect.y -= 100
                        dy_traning = 5
            if event.type == pygame.KEYUP:
                if event.key in (pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN):
                    x, y = 0, 0
        if dy_traning != 0:
            if start_y > hero_traning.rect.y:
                hero_traning.rect.y += dy_traning
            else:
                dy_traning = 0
        if pygame.sprite.collide_mask(coin_traning, hero_traning):
            coin_traning.kill()
            if coin1:
                coin_traning1 = Money(load_image("coin.png"), 6, 1, 30, level_traning.rect.y - 30)
                training_sprite.add(coin_traning1)
                coin1 = False
                coin2 = True
        if coin2:
            if pygame.sprite.collide_mask(coin_traning1, hero_traning):
                coin_traning1.kill()
                run = False
        if x != 0:
            hero_traning.update(x, y)
        coin_group.update()
        screen.fill(BLACK)
        training_sprite.draw(screen)
        screen.blit(text, (435, 210))
        screen.blit(text2, (375, 225))
        screen.blit(text3, (335, 240))
        clock.tick(FPS)
        pygame.display.flip()
    # этап №3 Жизни и выстрел
    hero_traning.kill()
    hero_traning = Hero_traning(load_image("hero.png"), 6, 1, 100, start_y)
    training_sprite.add(hero_traning)
    text = font.render('Молодец!', 1, WHITE)
    text2 = font.render('Следи за жизнями, получай очки,', 1, WHITE)
    text3 = font.render('Убивай монстров (пробел).', 1, WHITE)
    text4 = font.render('Желаю удачи в путешествии!', 1, WHITE)
    text5 = font.render('Справка - CTRL + H', 1, WHITE)
    text6 = font.render('(Нажми пробел для начала игры)', 1, WHITE)
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE):
                hero_traning.kill()
                run = False
                level_traning.kill()
        if dy_traning != 0:
            if start_y > hero_traning.rect.y:
                hero_traning.rect.y += dy_traning
            else:
                dy_traning = 0
        screen.fill(BLACK)
        training_sprite.draw(screen)
        for i in range(hero_traning.health):
            screen.blit(health_image, (420 + i * 35, 10))
        screen.blit(text, (380, 150))
        screen.blit(text2, (325, 165))
        screen.blit(text3, (350, 180))
        screen.blit(text4, (320, 195))
        screen.blit(text5, (350, 210))
        screen.blit(text6, (320, 225))
        clock.tick(FPS)
        pygame.display.flip()


def training_at_start():
    font = pygame.font.Font(None, 50)
    font1 = pygame.font.Font(None, 25)
    text = font.render('ОБУЧЕНИЕ', 1, (255, 255, 255))
    text1 = font1.render('Пройти обучение(SPACE)', 1, (255, 255, 255))
    text2 = font1.render('Пропустить(TAB)', 1, (255, 255, 255))
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_TAB:
                    return
                if event.key == pygame.K_SPACE:
                    training()
                    return
            screen.fill(BLACK)
            screen.blit(text, (200, 100))
            screen.blit(text1, (80, 300))
            screen.blit(text2, (330, 300))
            pygame.display.flip()


def restart():
    global hero_group, coin_group, islands_group, hero, hero_direction, \
        dragon_health, health_monsters_group, monsters_group, dragon
    for hero in hero_group:
        hero.kill()

    for dragon in monsters_group:
        dragon.kill()

    for dragon_health in health_monsters_group:
        dragon_health.kill()

    hero_group = pygame.sprite.Group()
    coin_group = pygame.sprite.Group()
    islands_group = pygame.sprite.Group()

    hero = Hero(load_image("hero.png"), 6, 1, 30, start_y)
    hero_direction = 'right'
    level.rect.x = 0
    dragon = Monster(load_image("dragon.png"), 8, 2, 400, 270)
    dragon_health = Health_monster(dragon)

    for i in range(len(coin_coords)):
        Money(load_image('coin.png'), 6, 1, coin_coords[i][0], coin_coords[i][1])

    for i in range(len(island_coords)):
        Island(island_coords[i][0], island_coords[i][1], island_coords[i][2])


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
hero = Hero(load_image('hero.png'), 6, 1, 100, 300)
dragon = Monster(load_image('dragon.png'), 8, 2, 400, 270)
dragon_health = Health_monster(dragon)
health_image = load_image('health.png', color_key=-1)
boom_image = load_image('boom.png', color_key=-1)
info_image = load_image('info.png')
start_y = level.rect.y - level.rect.height - 15

# Добавлять координаты монет
coin_coords = [(250, start_y), (350, start_y), (450, start_y)]

# Добавлять координаты и тип картинки островков
island_coords = [('classic_island', 200, 280), ('classic_island', 500, 230)]

clock = pygame.time.Clock()
FPS = 50
running = True
start_screen_show = True
show_info = False
x, y = 0, 0
dy = 0
hero_direction = 'right'
hero_health = hero.health
hero_score = hero.score
font_for_score = pygame.font.Font(None, 25)

background_image = load_image('country_field.png')

while running:
    if start_screen_show:
        start_screen()
        training_at_start()
        start_screen_show = False
        hero_group = pygame.sprite.Group()
        coin_group = pygame.sprite.Group()

        for i in range(len(coin_coords)):
            Money(load_image('coin.png'), 6, 1, coin_coords[i][0], coin_coords[i][1])

        for i in range(len(island_coords)):
            Island(island_coords[i][0], island_coords[i][1], island_coords[i][2])

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
                hero = Hero(load_image("hero.png"), 6, 1, x_d, y_d, health=hero.health, score=hero.score)

            if pygame.key.get_pressed()[pygame.K_UP] and pygame.key.get_pressed()[pygame.K_LEFT]:
                hero_direction = 'left'
                x, y = (-20, 0)
                x_d, y_d = hero.rect.x, hero.rect.y
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero_left.png"), 6, 1, x_d, y_d, health=hero.health, score=hero.score)

            if event.key == pygame.K_RIGHT:
                hero_direction = 'right'
                x, y = (10, 0)
                x_d, y_d = hero.rect.x, hero.rect.y
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero.png"), 6, 1, x_d, y_d, health=hero.health, score=hero.score)

            if event.key == pygame.K_LEFT:
                hero_direction = 'left'
                x_d, y_d = hero.rect.x, hero.rect.y
                hero_group = pygame.sprite.Group()
                hero = Hero(load_image("hero_left.png"), 6, 1, x_d, y_d, health=hero.health, score=hero.score)
                x, y = (-10, 0)
                print(level.rect.x)
            if event.key == pygame.K_UP:
                collide_flag = True
                if dy != 5:
                    hero.rect.y -= 100
                    dy = 5

            if event.key == pygame.K_SPACE:
                bullets_sound.play()
                Bullet(hero.rect.x, hero.rect.y, 'bullet.png')

            # Перезагрузка уровня при нажатии Ctrl + R
            if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_r]:
                restart()

            # Всплывающая подсказка
            if pygame.key.get_pressed()[pygame.K_LCTRL] and pygame.key.get_pressed()[pygame.K_h]:
                show_info = True
            elif event.key == pygame.K_h:
                show_info = False

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

    # Отрисовка жизней героя
    for i in range(hero.health):
        screen.blit(health_image, (420 + i * 35, 10))

    # Отображение очков героя
    text = font_for_score.render('Score' + ' ' + str(hero.score), 1, (255, 255, 255))
    screen.blit(text, (10, 10))

    # Если xp героя меньше, чем на предудущем шаге
    if hero_health != hero.health:
        screen.blit(boom_image, (dragon.rect.x - 50, dragon.rect.y - 50))
        hero_health = hero.health

    # Отрисовка групп спрайтов
    hero_group.draw(screen)
    levels_group.draw(screen)
    bullets_group.draw(screen)
    health_monsters_group.draw(screen)
    monsters_group.draw(screen)
    coin_group.draw(screen)
    islands_group.draw(screen)

    if show_info:
        screen.blit(info_image, (10, 100))

    # Обновление групп спрайтов
    bullets_group.update()
    monsters_group.update()
    coin_group.update()

    clock.tick(FPS)
    pygame.display.flip()
