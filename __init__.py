import sys
import pygame
import random
from pygame.locals import *

WIDTH = 640
HEIGHT = 480


class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/player.png")
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH / 2
        self.rect.centery = HEIGHT / 2

    def update(self):
        pos = pygame.mouse.get_pos()

        px = pos[0]
        py = pos[1]

        self.rect.left = px
        self.rect.top = py


class Square(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/square.png")
        self.rect = self.image.get_rect()

        x = random.randrange(1, 620)
        y = random.randrange(1, 460)

        while x == player_rect.top and y == player_rect.left:
            x = random.randrange(1, 620)
            y = random.randrange(1, 460)

        self.rect.centerx = x
        self.rect.centery = y


class Enemy(pygame.sprite.Sprite):
    def __init__(self, player_rect):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("images/enemy.png")
        self.rect = self.image.get_rect()

        x = random.randrange(10, 620)
        y = random.randrange(10, 460)
        s = random.randrange(1, 2)

        while x == player_rect.top and y == player_rect.left:
            x = random.randrange(10, 620)
            y = random.randrange(10, 460)

        self.rect.centerx = x
        self.rect.centery = y
        self.speed = [0.1, -0.1]

        if s == 1:
            self.speed = [0.1, -0.1]
        if s == 2:
            self.speed = [-0.1, 0.1]

    def actualizar(self, reloj):
        self.rect.centerx += self.speed[0] * reloj
        self.rect.centery += self.speed[1] * reloj

        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.speed[0] = -self.speed[0]
            self.rect.centerx += self.speed[0] * reloj
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed[1] = -self.speed[1]
            self.rect.centery += self.speed[1] * reloj


def load_image(filename, transparent=False):
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        image = image.convert()
        if transparent:
                color = image.get_at((0, 0))
                image.set_colorkey(color, RLEACCEL)
        return image


def main():
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Crazy Square")
    pygame.mouse.set_visible(False)
    clock = pygame.time.Clock()

    background_image = load_image('images/fondo.png')

    puntos = (0)
    fuente = pygame.font.Font("font/Bazar.ttf", 30)

    pygame.mixer.music.load("sound/sound.mp3")

    player = Player()
    square = Square(player.rect)
    enemigo = Enemy(player.rect)

    enemigos = []
    finish = False

    pygame.mixer.music.play(-1)

    while not finish:
        reloj = clock.tick(60)

        for eventos in pygame.event.get():
            if eventos.type == QUIT:
                sys.exit(0)

        player.update()
        for enemigo in enemigos:
            enemigo.actualizar(reloj)
            if pygame.sprite.collide_rect(enemigo, player):
                finish = True

        if pygame.sprite.collide_rect(square, player):
            square.rect.centerx = random.randrange(0, 620)
            square.rect.centery = random.randrange(0, 460)
            enemigos.append(Enemy(player.rect))
            puntos += 1

        screen.blit(background_image, (0, 0))
        screen.blit(square.image, square.rect)
        screen.blit(player.image, player.rect)
        for enemigo in enemigos:
            screen.blit(enemigo.image, enemigo.rect)

        puntuacion = fuente.render(str(puntos), 0, (255, 255, 255))
        screen.blit(puntuacion, (5, 5))

        pygame.display.flip()
    return 0

if __name__ == '__main__':
    pygame.init()
    main()
