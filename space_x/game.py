import math
import random
import pygame
from pygame import mixer


class MyGame:
    def __init__(self):
        pygame.init()

        # Screen Resolution
        self.screen_x = 1366
        self.screen_y = 760

        # Game Setup
        pygame.display.set_caption("Space Craft")
        mixer.music.load('space_x/audio/pubg.wav')
        mixer.music.play(-1)
        self.game_screen = pygame.display.set_mode((self.screen_x, self.screen_y))

        # Enemies
        self.source_enemy = ['alien_0.png', 'alien_1.png', 'alien_2.png', 'alien_3.png',
                             'alien_4.png', 'alien_5.png', 'alien_6.png']
        self.source_enemy_power = list()
        self.score_list = list()
        e_power = 0.5
        e_score = 1
        for i in range(len(self.source_enemy)):
            self.source_enemy_power.append(e_power)
            self.score_list.append(e_score)
            e_power += 0.2
            e_score += 0.5

        # UFO initial position
        self.ufo_icon = pygame.image.load('space_x/image/ufo.png')
        self.ufo_X = self.screen_x / 2
        self.ufo_Y = self.screen_y - 150
        self.ufo_X_change = 0

        # Enemy initial position
        self.enemy_icon = [pygame.image.load("space_x/image/"+data) for data in self.source_enemy]
        self.enemy_X = [0] * len(self.source_enemy)
        self.enemy_Y = [20] * len(self.source_enemy)
        self.enemy_X_change = self.source_enemy_power.copy()
        self.enemy_Y_change = [64] * len(self.source_enemy)

        # Bullet Initial Positions
        self.bullet_icon = pygame.image.load('space_x/image/bullet.png')
        self.bullet_X = 0
        self.bullet_Y = self.screen_y - 150
        self.bullet_X_change = 0
        self.bullet_Y_change = 2
        self.bullet_state = 'ready'

        # Initial Parameters
        self.game_running = True
        self.upgrade_score = 10
        self.enemy_approch = 64
        self.score = 0
        self.no_of_enemies = 1

    def player(self, pos_x, pos_y):
        game_icon = pygame.image.load('space_x/image/ufo.png')
        self.game_screen.blit(game_icon, (pos_x, pos_y))

    def enemy(self, pos_x, pos_y, index):
        self.game_screen.blit(self.enemy_icon[index], (pos_x, pos_y))

    def fire_bullet(self, pos_x, pos_y):
        self.bullet_state = 'fire'
        self.game_screen.blit(self.bullet_icon, (pos_x + 16, pos_y + 10))

    def show_score(self):
        font = pygame.font.Font('freesansbold.ttf', 22)
        score_text = font.render("Score: " + str(self.score) + " / " + str(self.upgrade_score), True, (255, 255, 255))
        self.game_screen.blit(score_text, (10, 10))

    def upgrade_level(self):
        if self.score >= self.upgrade_score:
            if self.no_of_enemies < len(self.source_enemy):
                self.no_of_enemies += 1
            self.bullet_Y_change += 2
            if self.upgrade_score == 10:
                self.upgrade_score += 20
            elif self.upgrade_score >= 30:
                self.upgrade_score += 50
            self.enemy_approch += 15

    def game_over(self):
        g_font = pygame.font.Font('freesansbold.ttf', 62)
        game_over_text = g_font.render("GAME OVER", True, (255, 255, 255))
        self.game_screen.blit(game_over_text, (self.screen_x / 2 - 150, self.screen_y / 2 - 100))
        mixer.music.stop()

    @staticmethod
    def is_collide(enemy_x, enemy_y, bullet_x, bullet_y):
        distance = math.sqrt(
            math.pow(enemy_x - bullet_x, 2) + math.pow(enemy_y - bullet_y, 2))
        if distance < 27:
            return True
        else:
            return False

    def play_game(self):
        while self.game_running:
            self.game_screen.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.game_running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        try:
                            self.ufo_X_change = - self.source_enemy_power[i] - 0.5
                        except:
                            self.ufo_X_change = - self.source_enemy_power[0]
                    if event.key == pygame.K_RIGHT:
                        try:
                            self.ufo_X_change = self.source_enemy_power[i] + 0.5
                        except:
                            self.ufo_X_change = self.source_enemy_power[0] + 0.5
                    if event.key == pygame.K_SPACE and self.bullet_state == 'ready':
                        bullet_sound = mixer.Sound('space_x/audio/laser.wav')
                        bullet_sound.play()
                        self.bullet_X = self.ufo_X
                        self.fire_bullet(self.bullet_X, self.bullet_Y)
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                        self.ufo_X_change = 0

            self.ufo_X += self.ufo_X_change
            if self.ufo_X < 0:
                self.ufo_X = 0
            elif self.ufo_X > self.screen_x - 64:
                self.ufo_X = self.screen_x - 64

            for i in range(self.no_of_enemies):
                if self.enemy_Y[i] > self.screen_y - 200:
                    for j in range(self.no_of_enemies):
                        self.enemy_Y[j] = 2000
                    self.game_over()
                    break

                collide = self.is_collide(self.enemy_X[i], self.enemy_Y[i], self.bullet_X, self.bullet_Y)
                if collide:
                    explose_sound = mixer.Sound('space_x/audio/explosion.wav')
                    explose_sound.play()
                    self.bullet_Y = self.screen_y - 150
                    self.bullet_state = 'ready'
                    self.score += self.score_list[self.enemy_icon.index(self.enemy_icon[i])]
                    self.enemy_X[i] = random.randint(0, self.screen_x - 64)
                    self.enemy_Y[i] = self.screen_y - (self.screen_y - 20)
                    self.upgrade_level()

                self.enemy(self.enemy_X[i], self.enemy_Y[i], i)

                self.enemy_X[i] += self.enemy_X_change[i]
                if self.enemy_X[i] <= 0:
                    self.enemy_X_change[i] = self.source_enemy_power[self.enemy_icon.index(self.enemy_icon[i])]
                    self.enemy_Y[i] += self.enemy_approch
                elif self.enemy_X[i] > self.screen_x - 64:
                    self.enemy_X_change[i] = - self.source_enemy_power[self.enemy_icon.index(self.enemy_icon[i])]
                    self.enemy_Y[i] += self.enemy_approch

            if self.bullet_Y < 0:
                self.bullet_Y = self.screen_y - 150
                self.bullet_state = 'ready'

            if self.bullet_state == 'fire':
                self.fire_bullet(self.bullet_X, self.bullet_Y)
                self.bullet_Y -= self.bullet_Y_change

            self.player(self.ufo_X, self.ufo_Y)
            self.show_score()
            pygame.display.update()
