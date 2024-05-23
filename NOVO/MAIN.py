import copy
import pygame
import math
from tabuleiro import tabuleiro
from sprite import *
from Move import *
from colisões import *
import sys
pygame.init()

SCREEN = pygame.display.set_mode((1280, 720))
LARGURA = 800
ALTURA = 600
tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("PacMenke")


WIDTH = 900
HEIGHT = 950
screen = pygame.display.set_mode([WIDTH, HEIGHT])

fps = 60
font = pygame.font.Font('freesansbold.ttf', 20)
level = copy.deepcopy(tabuleiro)
color = 'blue'
PI = math.pi

sdt_sfx = pygame.mixer.Sound("assets/kahoot.mp3")
sdt_sfx.play()
#Imagens do pacMenke
imagens_jog = []
for i in range(1, 5):
    imagens_jog.append(pygame.transform.scale(pygame.image.load(f'assets/{i}.png'), (45, 45)))
#Imagens dos humbertasmas
blinky_img = pygame.transform.scale(pygame.image.load(f'assets/blue.png'), (45, 45))
pinky_img = pygame.transform.scale(pygame.image.load(f'assets/blue.png'), (45, 45))
inky_img = pygame.transform.scale(pygame.image.load(f'assets/blue.png'), (45, 45))
clyde_img = pygame.transform.scale(pygame.image.load(f'assets/blue.png'), (45, 45))
spooked_img = pygame.transform.scale(pygame.image.load(f'assets/powerup.png'), (45, 45))
dead_img = pygame.transform.scale(pygame.image.load(f'assets/dead.png'), (45, 45))
jogador_x = 450
jogador_y = 663
direction = 0
blinky_x = 56
blinky_y = 58 
direcao_blinky = 0
inky_x = 440
inky_y = 388
inky_direction = 2
pinky_x = 440
pinky_y = 438
direcao_pinky = 2
clyde_x = 440
clyde_y = 438
direcao_clyde = 2
counter = 0
flicker = False

turns_allowed = [False, False, False, False]
direction_command = 0
player_speed = 2
score = 0
powerup = False
power_counter = 0
eaten_ghost = [False, False, False, False]
metas = [(jogador_x, jogador_y), (jogador_x, jogador_y), (jogador_x, jogador_y), (jogador_x, jogador_y)]
blinky_dead = False
inky_dead = False
clyde_dead = False
pinky_dead = False
blinky_box = False
inky_box = False
clyde_box = False
pinky_box = False
moving = False
ghost_speeds = [2, 2, 2, 2]
startup_counter = 0
lives = 3
game_over = False
game_won = False


def tabuleirodes():
    num1 = ((HEIGHT - 50) // 32)
    num2 = (WIDTH // 30)
    for i in range(len(level)):
        for j in range(len(level[i])):
            if level[i][j] == 1:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 4)
            if level[i][j] == 2 and not flicker:
                pygame.draw.circle(screen, 'white', (j * num2 + (0.5 * num2), i * num1 + (0.5 * num1)), 10)
            if level[i][j] == 3:
                pygame.draw.line(screen, color, (j * num2 + (0.5 * num2), i * num1), (j * num2 + (0.5 * num2), i * num1 + num1), 3)
            if level[i][j] == 4:
                pygame.draw.line(screen, color, (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)
            if level[i][j] == 5:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 + (0.5 * num1)), num2, num1], 0, PI / 2, 3)
            if level[i][j] == 6:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 + (0.5 * num1)), num2, num1], PI / 2, PI, 3)
            if level[i][j] == 7:
                pygame.draw.arc(screen, color, [(j * num2 + (num2 * 0.5)), (i * num1 - (0.4 * num1)), num2, num1], PI, 3 * PI / 2, 3)
            if level[i][j] == 8:
                pygame.draw.arc(screen, color, [(j * num2 - (num2 * 0.4)) - 2, (i * num1 - (0.4 * num1)), num2, num1], 3 * PI / 2, 2 * PI, 3)
            if level[i][j] == 9:
                pygame.draw.line(screen, 'white', (j * num2, i * num1 + (0.5 * num1)), (j * num2 + num2, i * num1 + (0.5 * num1)), 3)

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(imagens_jog[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Agora o Menke não sairá no Fim de Semana! Pressione a barra de espaço para restartar!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Menke sairá no Fim de Semana! Pressione a barra de espaço para restartar!', True, 'green')
        screen.blit(gameover_text, (100, 300))

def draw_misc():
    score_text = font.render(f'Score: {score}', True, 'white')
    screen.blit(score_text, (10, 920))
    if powerup:
        pygame.draw.circle(screen, 'blue', (140, 930), 15)
    for i in range(lives):
        screen.blit(pygame.transform.scale(imagens_jog[0], (30, 30)), (650 + i * 40, 915))
    if game_over:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Agora o Menke não sairá no Fim de Semana! Pressione a barra de espaço para restartar!', True, 'red')
        screen.blit(gameover_text, (100, 300))
    if game_won:
        pygame.draw.rect(screen, 'white', [50, 200, 800, 300],0, 10)
        pygame.draw.rect(screen, 'dark gray', [70, 220, 760, 260], 0, 10)
        gameover_text = font.render('Menke sairá no Fim de Semana! Pressione a barra de espaço para restartar!', True, 'green')
        screen.blit(gameover_text, (100, 300))       
    