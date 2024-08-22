#Baseado em tutorial de https://coderslegacy.com/python/python-pygame-tutorial/ com alguma modificações feitas

#Room for improvement: Reiniciar depois da tela de Game Over

import pygame, sys
from pygame.locals import *
import random, time

pygame.init()

#Definindo FPS
FPS = 60
FramesPerSec = pygame.time.Clock()

#Predefinindo Cores
BLUE  = (0, 0, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#Variáveis
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 10
PSPEED = 5
SCORE = 0

#Criando uma tela com plano de fundo
DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
DISPLAYSURF.fill(WHITE)
bakcground = pygame.image.load("sources\AnimatedStreet.png")
pygame.display.set_caption("Game")                  # nome que aparece no título da janela

#Predefinindo Fontes
font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
font_in_game_score = pygame.font.SysFont("Verdana", 28)
game_over = font.render("Game Over", True, BLACK)
show_scores = font_small.render("Score: ", True, BLACK)

#definimos a música de fundo
pygame.mixer.music.load(r'sources\background.wav')
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)                         # a música que carregamos no inínio irá tocar indefinitivamente

class Background():                                 # classe para fazer o background
    def __init__(self):
        self.bgimage = pygame.image.load("sources\AnimatedStreet.png")          # definimos a imagem do bg 
        self.rectBGimg = self.bgimage.get_rect()                                # pegamos o rect da imagem

        self.bgY1 = 0                               # criamos as coordenadas das duas cópias do bg
        self.bgX1 = 0
        self.bgY2 = -self.rectBGimg.height          # a cópia fica 'em cima' da original
        self.bgX2 = 0

        self.movingUpSpeed = PSPEED                 # o bg vai se movimentar de acordo com a velocidade do player      

    def update(self):                               # função para atualizar o bg
        self.bgY1 += self.movingUpSpeed                                         # a lógica é:
        self.bgY2 += self.movingUpSpeed                                         # os dois bg se movem juntos (a posição deles começa no 0)
        if self.bgY1 >= self.rectBGimg.height:                                  # se a posição for maior do que a 'altura' do rect
            self.bgY1 = -self.rectBGimg.height                                  # o bg é resetado para em cima do posição da original da linha 52
        if self.bgY2 >= self.rectBGimg.height:                                  # o mesmo para a cópia
            self.bgY2 = -self.rectBGimg.height                                  # assim sempre vai ter um bg na posição original e outro na cópia
    
    def render(self):                               # blit dos backgrounds
        DISPLAYSURF.blit(self.bgimage, (self.bgX1, self.bgY1))
        DISPLAYSURF.blit(self.bgimage, (self.bgX2, self.bgY2))

class Player(pygame.sprite.Sprite):                 # ao passar a classe Sprite como parâmetro da classe Player nós fazemos com que Player seja uma child class de Sprite
    def __init__(self):
        super().__init__()                          # init de Sprite
        self.image = pygame.image.load("sources\Player.png")
        self.rect = self.image.get_rect()           # cria um retângulo do mesmo tamanho da imagem que servirá para a colisão
        self.rect.center = (160,520)                # define um ponto inicial para o rect. Se não tomar cuidado pode acabar com o Rect em um canto diferente da imagem

    def move(self):                                 # função para controlar a movimentação do player
        pressed_keys = pygame.key.get_pressed()     
        if self.rect.top > 0:                       # apenas se move para a esquerda caso não esteja "colado" na borda
            if pressed_keys[K_UP]:
                self.rect.move_ip(0,-PSPEED)
                
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_DOWN]:
                self.rect.move_ip(0,PSPEED)

        if self.rect.left > 0:                      
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-PSPEED,0)
        
        if self.rect.right < SCREEN_WIDTH:          
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(PSPEED,0)
    '''                                                 # substituimos a função draw ao criarmos grupos de classes
    def draw(self, surface):
        surface.blit(self.image, self.rect)         # blit server para desenhar uma surface em cima da outra. No caso, usamos o sprite como o parâmetro da surface
                                                    # uma surface é qualquer texto, imagem ou objeto que vc criar, inclusive o próprio display
    '''        
#Player

'''
class Player_2(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("sources\Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160,520)

    def update(self):
        pressed_keys = pygame.key.get_pressed()
        if self.rect.top > 0:
            if pressed_keys[K_w]:
                self.rect.move_ip(0,-5)
                
        if self.rect.bottom < SCREEN_HEIGHT:
            if pressed_keys[K_s]:
                self.rect.move_ip(0,5)

        if self.rect.left > 0:              
            if pressed_keys[K_a]:
                self.rect.move_ip(-5,0)
        
        if self.rect.right < SCREEN_WIDTH:  
            if pressed_keys[K_d]:
                self.rect.move_ip(5,0)

    def draw(self, surface):
        surface.blit(self.image, self.rect)

#Player2
'''

class Enemy(pygame.sprite.Sprite):                  # também será fila da classe Sprite
    def __init__(self):             
        super().__init__()                          # init da classe Sprite
        self.image = pygame.image.load("sources\Enemy.png")
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40,SCREEN_WIDTH-40),0)           # um randomizador para onde ela será gerada.
                                                                            # é escolhido um número aleatório entre 40 e 360 (margens da tela)
                                                                            # esse número aleatório é passado como a coordenada do eixo x para o centro do rect

    def move(self):
        global SCORE
        self.rect.move_ip(0,SPEED)                  # move o objeto SPEED pixels para baixo

        if (self.rect.top > 900):                                           # se o topo do objeto alcnça a borda da tela ele é 'resetado' para um ponto aleatório dentro do limite no topo da tela e aumentamos o score em 1
            SCORE += 1                                                      # escolhemos o topo para dar o efeito de 'continuar' na borda da tela ao invés de apenas desaparecer
            self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)     

    '''                                                 # substituimos a função draw ao criarmos grupos de classes
    def draw(self, surface):
        surface.blit(self.image, self.rect)         # blit para desenhar a surface
    '''

#Enemy

P1 = Player()
#P2 = Player_2()
E1 = Enemy()
back_ground = Background()

enemies = pygame.sprite.Group()                     # criamos grupos de classes Sprite para que possamos tratá-las mais facilmente (ao invés de uma por uma, tratamos o grupo)
enemies.add(E1)
all_sprites = pygame.sprite.Group()
all_sprites.add(E1, P1)

INC_SPEED = pygame.USEREVENT + 1                    # criamos um evento personalizado com a propriedade USEREVENT e adicionamos 1 para que tenha um id único (ver resumo #USER EVENTS)                                        
pygame.time.set_timer(INC_SPEED, 1000)              # fazemos uma chamada para o evento a cada 1s

while True:
    for event in pygame.event.get():                # captura os eventos que acontecem
        if event.type == INC_SPEED:                 # se for evento do tipo INC_SPEED a variável SPEED é aumentada em 2
            SPEED += 0.5

        if event.type == QUIT:                      # se for evento do tipo quit o pygame é encerrado e o sistema é limpo
            pygame.quit()
            sys.exit()                
    

    DISPLAYSURF.fill(BLACK)                         # define o Surface do display
                                                    # cuidado para não deixar essa linha por último e criar apenas uma 'camada' branca acima dos outros sprites
    DISPLAYSURF.blit(bakcground, (0,0))             # posicionamos a tela de fundo
    
    back_ground.update()
    back_ground.render()
    
    in_game_scores = font_in_game_score.render(str(SCORE), True, BLACK)                         # criamos e posicionamos uma surface para os scores do jogador. Fazemos isso no Loop pois é algo que vai ser atualizado constantemente.
    DISPLAYSURF.blit(in_game_scores,(10,10))
                                                    # lembrando do sistemas de camada do PyGame

    if pygame.sprite.spritecollideany(P1, enemies):                             # usamos o método collideany para checar se alguma sprite colidiu com outra (ver resumo #COLLISION)
        pygame.mixer.music.stop()                                               # paramos a música
        pygame.mixer.Sound("sources\crash.wav").play()                          # criamos o objeto para o som de batida e damos play
        time.sleep(1)                                                           # 1 segundo de 'tela congelada'
        DISPLAYSURF.fill(RED)                                                   # colocamos uma tela vermelha
        DISPLAYSURF.blit(game_over,(30,250))                                    # mostramos a mensagem de Game Over
        DISPLAYSURF.blit(show_scores, (150, 350))
        scores = font_small.render(str(SCORE), True, BLACK)                     # iniciamos o surface para os scores na tela de game over
        DISPLAYSURF.blit(scores, (230,350))                                     # mostramos a pontuação do jogador
        pygame.display.update()
        time.sleep(2)
        for entity in all_sprites:                                              # todas as entidades são apagadas
            entity.kill()   
        pygame.quit()
        sys.exit()

    for entity in all_sprites:                      # com grupos também podemos substituir as funções de draw para um blit geral de todas as sprites do grupo
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()
        

    #P1.update()                                    # não é mais necessário graças aos grupos
    #P2.update()
    #E1.move()                                      # não é mais necessário graças aos grupos


    #P1.draw(DISPLAYSURF)                           # chama as funções de draw para o surface display    ! não é mais necessário graças aos grupos !
    #P2.draw(DISPLAYSURF)
    #E1.draw(DISPLAYSURF)

    pygame.display.update()                         # atualiza o display com os eventos do loop
    FramesPerSec.tick(FPS)                          # limita o FPS para que só faça 60 loops em 1s 