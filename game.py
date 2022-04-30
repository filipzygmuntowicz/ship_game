import pygame
import random
import os

LIVES = 25
screen_width = 1024
screen_height = 768

pygame.init()
clock = pygame.time.Clock()
pygame.display.set_caption('Show Text')
font = pygame.font.Font('freesansbold.ttf', 32)

# Star - obiekt jednej gwiazdy z tła


class Star:
    def __init__(self, position_x, position_y, distance, direction, speed, size,
                 color):
        self.position_x = position_x
        self.position_y = position_y
        self.distance = distance
        self.size = size
        self.direction = direction
        self.speed = speed
        self.color = (int(distance * color[0]),
                      int(distance * color[1]),
                      int(distance * color[2]))

    def draw(self, display):
        self.color = [(self.color[0]*3) % 255, (self.color[0]*3) %
                      255, (self.color[0]*3) % 255]
        display.fill(self.color, (self.position_x, self.position_y,
                                  self.size, self.size))

    def erase(self, display):
        display.fill((0, 0, 0), (self.position_x, self.position_y,
                                 self.size, self.size))

    def move(self, elapsed_time):
        self.position_x += (self.direction*self.speed * elapsed_time)

    def set_direction(self, new_direction):
        self.direction = new_direction

    def set_speed(self, new_speed):
        self.speed = new_speed
# Starfield - zbiór obiektów Star


class Starfield:
    def __init__(self, display, rect, number_of_stars, direction,
                 speed_sequence, size, color=(255, 255, 255)):
        self.display_surface = display
        self.display_rect = rect
        self.direction = direction
        self.fastest_star_speed = speed_sequence[0]
        self.slowest_star_speed = speed_sequence[1]
        self.brightest_color = color
        self.number_of_stars = number_of_stars
        self.timer = Timer()
        self.stars = []
        for i in range(number_of_stars):
            x_pos = self.random_x()
            y_pos = self.random_y()
            distance = random.random()
            speed = ((distance *
                      (self.fastest_star_speed - self.slowest_star_speed)) +
                     self.slowest_star_speed)
            my_star = Star(x_pos, y_pos, distance,
                           direction, speed, size, color)
            self.stars.append(my_star)

    def update(self):
        self.erase()
        self.move()
        self.draw()

    def draw(self):
        for my_star in self.stars:
            my_star.draw(self.display_surface)

    def erase(self):
        for my_star in self.stars:
            my_star.erase(self.display_surface)

    def move(self):
        elapsed_time = self.timer.get_elapsed_time()
        for my_star in self.stars:
            my_star.move(elapsed_time)
            if my_star.position_x <= self.display_rect.left:
                my_star.position_x = self.display_rect.right
                my_star.position_y = self.random_y()
            elif my_star.position_x >= self.display_rect.right:
                my_star.position_x = self.display_rect.left
                my_star.position_y = self.random_y()

            if my_star.position_y <= self.display_rect.top:
                my_star.position_y = self.display_rect.bottom
                my_star.position_x = self.random_x()
            elif my_star.position_y >= self.display_rect.bottom:
                my_star.position_y = self.display_rect.top
                my_star.position_x = self.random_x()

    def set_direction(self, new_direction):
        self.direction = new_direction
        for star in self.stars:
            star.set_direction(new_direction)
        return

    def set_speeds(self, new_speed_sequence):
        self.fastest_star_speed = new_speed_sequence[0]
        self.slowest_star_speed = new_speed_sequence[1]
        for star in self.stars:
            new_speed = ((star.distance *
                         (self.fastest_star_speed-self.slowest_star_speed)) +
                         self.slowest_star_speed)
            star.set_speed(new_speed)

    def random_x(self):
        return float(random.randint(self.display_rect.left, self.display_rect.right))

    def random_y(self):
        return float(random.randint(self.display_rect.top, self.display_rect.bottom))


class Timer:
    def __init__(self):
        self.current_time = pygame.time.get_ticks()

    def get_elapsed_time(self):
        now = pygame.time.get_ticks()
        elapsed_time = (now - self.current_time) * 0.001
        self.current_time = now
        return elapsed_time


ship_size = (1*(screen_width/6), 576*(screen_height/6)/1024)
# Player - obiekt gracz


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, LIVES, stunned=False):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship.png'), ship_size))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship2.png'), ship_size))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship3.png'), ship_size))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship4.png'), ship_size))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship5.png'), ship_size))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        self.LIVES = LIVES
        self.stunned = stunned

    def update(self, warp, direction):
        if warp == 0:
            self.current_sprite = 4
        else:
            self.current_sprite += 1
            if self.current_sprite >= len(self.sprites)-1:
                self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        if direction == 1:

            self.image = pygame.transform.rotate(self.image, 180)

    def lose_life(self):
        if self.LIVES > 0:
            self.LIVES = self.LIVES - 1
        if self.LIVES == 0:
            if self.alive():
                bs1 = broken_ship(self.rect.x, self.rect.y,
                                  os. getcwd()+'/sprites/ship_broken.png')
                bs2 = broken_ship(self.rect.x, self.rect.y,
                                  os. getcwd()+'/sprites/ship_broken2.png')
                moving_sprites_broken_ship.add(bs1)
                moving_sprites_broken_ship.add(bs2)
            self.kill()


ship_size2 = (1*(screen_width/5.2), 576*(screen_height/5.)/1024)
# Enemy - statek wyprzedzający gracza


class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship_enemy.png'), ship_size2))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship_enemy2.png'), ship_size2))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship_enemy3.png'), ship_size2))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/ship_enemy4.png'), ship_size2))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self, warp, direction):
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        if warp > 4:
            self.image = pygame.transform.scale(self.sprites[self.current_sprite], [
                                                ship_size2[0]*0.7, ship_size2[1]*0.7])
            if self.rect.x > -screen_width/2:
                self.rect.x = self.rect.x-screen_width/100
        elif warp < 4:
            self.image = pygame.transform.scale(self.sprites[self.current_sprite], [
                                                ship_size2[0]*1.5, ship_size2[1]*1.5])
            if self.rect.x < screen_width*1.4:
                self.rect.x = self.rect.x+screen_width/100
        elif warp == 4:
            self.image = self.sprites[self.current_sprite]
        if random.randint(1, 20) == 4:
            self.rect.y = self.rect.y+random.choice([-1, 1])*screen_height/500
        if direction == 1:
            self.image = pygame.transform.rotate(self.image, 180)

# photon_torpedo1 i 2 - lecące w stronę gracza torpedy fotonowe


torpedo_size = (960*(screen_width/12)/560, (screen_height/12))
torpedo_size2 = (791*(screen_width/12)/351, (screen_height/12))


class photon_torpedo(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/torpeda11.png'), torpedo_size))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/torpeda12.png'), torpedo_size))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self, warp, direction):
        warp = warp*direction
        if self.rect.x > -screen_width/20:
            self.rect.x = self.rect.x - \
                (screen_width/80+screen_width*random.random() /
                 125+(screen_width/1000)*(-warp))
        else:
            self.rect.x = screen_width
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        if pygame.sprite.collide_rect(self, player):
            player.lose_life()


class photon_torpedo2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.sprites = []
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/torpeda21.png'), torpedo_size2))
        self.sprites.append(pygame.transform.scale(
            pygame.image.load(os. getcwd()+'/sprites/torpeda22.png'), torpedo_size2))
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def update(self, warp, direction):
        warp = warp*direction
        if self.rect.x > -screen_width/30:
            self.rect.x = self.rect.x - \
                (screen_width/80+screen_width*random.random() /
                 125+(screen_width/1000)*(-warp))
        else:
            self.rect.x = screen_width
        self.current_sprite += 1
        if self.current_sprite >= len(self.sprites):
            self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]
        if pygame.sprite.collide_rect(self, player):
            player.stunned = True


# broken_ship- statek przy utracie wszystkich żyć rozpada się na dwa sprite'y będące tymi obiektami

broken_ship_size = (1*(screen_width/6), 576*(screen_height/6)/1024)


class broken_ship(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, part):
        super().__init__()
        self.part = part
        self.image = pygame.transform.scale(
            pygame.image.load(str(self.part)), broken_ship_size)
        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        a = random.choice([-1, 1])
        if part == os. getcwd()+'/sprites/ship_broken.png':
            self.direction = a
        if part == os. getcwd()+'/sprites/ship_broken2.png':
            self.direction = -a

    def update(self):
        self.rect.x = self.rect.x+self.direction*screen_width/700
        self.rect.y = self.rect.y+self.direction*screen_height/500
        if abs(self.rect.x) > screen_width*1.5 or abs(self.rect.y) > screen_height or player.alive():
            self.kill()

# Tworzenie gwiazd z tła


NUMBER_OF_STARS = 250
CLOSEST_STAR_COLOR = (255, 255, 255)
STAR_SIZE_IN_PIXELS = 1
preset_speeds = ((0, 0), (30, 3), (50, 5), (90, 9), (160, 16),
                 (250, 25), (400, 40), (600, 60), (1000, 100), (1500, 150))
current_speed = 4
screen = pygame.display.set_mode(
    (screen_width, screen_height), pygame.SWSURFACE)
direction = -1
my_starfield = Starfield(screen, screen.get_rect(), NUMBER_OF_STARS, direction,
                         preset_speeds[current_speed],
                         STAR_SIZE_IN_PIXELS, CLOSEST_STAR_COLOR)


# Tworzenie obiektów gracza, przeciwnika i torped a także definiowanie nieruchomej galaktyki i game over

moving_sprites = pygame.sprite.Group()
moving_sprites_enemy = pygame.sprite.Group()
moving_sprites_torp1 = pygame.sprite.Group()
moving_sprites_torp2 = pygame.sprite.Group()
moving_sprites_broken_ship = pygame.sprite.Group()

player = Player(ship_size[0]/2, ship_size[1], LIVES)
enemy = Enemy(ship_size[0]/2, ship_size[1]*7)
torp1 = photon_torpedo(screen_width, screen_height*2)
torp2 = photon_torpedo2(screen_width*1.65, screen_height*2)

moving_sprites.add(player)
moving_sprites_enemy.add(enemy)
moving_sprites_torp1.add(torp1)
moving_sprites_torp2.add(torp2)

nebula = pygame.image.load(os. getcwd()+'/sprites/nebula.png')
nebula = pygame.transform.scale(nebula, (screen_width/3, screen_height/3))
neb_x = enemy.rect.x
neb_y = enemy.rect.y
game_over = pygame.image.load(os. getcwd()+'/sprites/game_over.png')
score = 0
while True:
    pygame.display.update()
    keys = pygame.key.get_pressed()
    if current_speed != 0:
        # Ruch gracza w prawo
        if keys[pygame.K_d]:
            if player.rect.x < screen_width:
                player.rect.x = player.rect.x+screen_width/80
        # Ruch gracza w lewo
        if keys[pygame.K_a]:
            if player.rect.x > 0:
                player.rect.x = player.rect.x-screen_width/80
        # Ruch gracza do góry
        if keys[pygame.K_w]:
            if player.rect.y > 0:
                player.rect.y = player.rect.y-screen_width/80
        # Ruch gracza w dół
        if keys[pygame.K_s]:
            if player.rect.x < screen_height:
                player.rect.y = player.rect.y+screen_width/80
        # Restart gry
        if keys[pygame.K_r] and player.alive() == False:
            enemy.rect.x = ship_size[0]/2
            moving_sprites.add(player)
            player.LIVES = 25
            score = 0
    for event in pygame.event.get():
        if event.type is pygame.QUIT:
            raise SystemExit
        if event.type == pygame.KEYDOWN:
            # Wyjście z gry
            if event.key == pygame.K_q:
                raise SystemExit
            # Zmnniejszenie prędkości przesuwania tła
            if event.key == pygame.K_KP4 or event.key == pygame.K_4:
                if current_speed >= 1:
                    current_speed -= 1
                    new_speed = preset_speeds[current_speed]
                    my_starfield.set_speeds(new_speed)
                    player.stunned = False
            # Zastopowanie przesuwania tła
            if event.key == pygame.K_KP5 or event.key == pygame.K_5:
                current_speed = 0
                new_speed = preset_speeds[current_speed]
                my_starfield.set_speeds(new_speed)
            # Zwiększenie prędkości przesuwania tła
            if event.key == pygame.K_KP6 or event.key == pygame.K_6:
                if current_speed <= 8:
                    current_speed += 1
                    new_speed = preset_speeds[current_speed]
                    my_starfield.set_speeds(new_speed)
                    player.stunned = False
            # Odwrócenie kierunku przesuwania tła
            if event.key == pygame.K_KP8 or event.key == pygame.K_8:
                direction = direction*(-1)
                my_starfield.set_direction(direction)
    # Generowannie pozycji lecących torped (szybkość torped zależy od prędkości przesuwania tła)
    if torp1.rect.x >= screen_width:
        torp1.rect.y = random.random()*screen_height
    if torp2.rect.x >= screen_width:
        torp2.rect.y = random.random()*screen_height
        if abs(torp2.rect.y-torp1.rect.y) < screen_height/20:
            torp2.rect.y = random.random()*screen_height
            if abs(torp2.rect.y-torp1.rect.y) < screen_height/20:
                torp2.rect.y = random.random()*screen_height
    screen.fill((0, 0, 0))
    # Rysowanie galaktyki, gwiazd, torped i ewentualnie rozwalonego statku
    screen.blit(nebula, (neb_x, neb_y))
    my_starfield.update()
    moving_sprites_torp1.draw(screen)
    moving_sprites_torp2.draw(screen)
    moving_sprites_torp1.update(current_speed, direction)
    moving_sprites_torp2.update(current_speed, direction)
    moving_sprites_broken_ship.draw(screen)
    moving_sprites_broken_ship.update()
    # Przy trafieniu niebieską torpedą silniki w statku wyłączają się
    if player.stunned == True:
        current_speed = 0
        new_speed = preset_speeds[current_speed]
        my_starfield.set_speeds(new_speed)
    # Jeśli przeciwnik wyprzedza gracza to jego statek jest rysowany po graczu i odwrotnie
    if current_speed <= 4:
        moving_sprites.draw(screen)
        moving_sprites.update(current_speed, direction)
        moving_sprites_enemy.draw(screen)
        moving_sprites_enemy.update(current_speed, direction)
    else:
        moving_sprites_enemy.draw(screen)
        moving_sprites_enemy.update(current_speed, direction)
        moving_sprites.draw(screen)
        moving_sprites.update(current_speed, direction)
    # Game over
    if player.alive() == False:
        go_x = screen_width/12
        go_y = screen_height/6
        screen.blit(game_over, (go_x, go_y))
    # Kalkulacja wyniku, im szybciej przesuwa się tło tym lepszy wynik i odwrotnie. Jeśli statek leci w przeciwnym kierunku to wynik maleje (bo torpedy są wolniejsze)
    if player.alive() and round(pygame.time.get_ticks()/100, 0) % 2 == 0:
        if current_speed == 0:
            score = score + 5
        else:
            score = score + (-1)*direction*current_speed
    # Rysowanie ilości żyć i wyniku
    text = font.render(
        'SCORE:' + str(score).replace(".0", ""), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (screen_width/10, screen_height/25)
    screen.blit(text, textRect)
    text = font.render('LIVES: '+str(player.LIVES), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (screen_width/2, screen_height/25)
    screen.blit(text, textRect)
    pygame.display.flip()
    clock.tick(60)
