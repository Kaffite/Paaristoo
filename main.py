"""
SNAKE WARS

Mängu tegid: Karl-Markus Hannust ja Robert Palm

NB: Mängu käivitamiseks on vaja mängu tausta, tegelase pildifaile ja veidi muid pildifaile ning pygame moodulit.

Nupud:
W, A, S, D -Liikumine
SPACE - tulistamine
P - mängu pausile panemine

Pygamesi baasiks ja õppimiseks kasutasime - 
https://www.youtube.com/watch?v=y9VG3Pztok8

Mängu tegelased ja muud võtsime lehelt, millel oli CC0 litsents.
https://opengameart.org/content/platformer-art-complete-pack-often-updated
"""
import pygame
import time
import random

pygame.init()

screen_width, screen_height =  1600, 1060
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60

platform_length = 400
platform_width = 45
small_length = 300

deep_length = 300
deep_length_mid = 500
deep_width = 450

# X start, Y start, X pikkus, Y laius
#platformd põhjas
platform_1 = pygame.Rect(500, 800 , deep_length_mid, deep_width)
platform_2 = pygame.Rect(100, 600, deep_length, deep_width)
platform_3 = pygame.Rect(1100,600, deep_length, deep_width)

#platformid taevas
platform_4 = pygame.Rect(50, 200 , platform_length, platform_width)
platform_5 = pygame.Rect(1050, 200 , platform_length, platform_width)
platform_6 = pygame.Rect(600, 400 , small_length, platform_width)

platform_image = pygame.image.load('grass.png')
platform_image = pygame.transform.scale(platform_image, (platform_length, platform_width))
platform_image_small =  pygame.transform.scale(platform_image, (small_length, platform_width))
platform_image_deep = pygame.transform.scale(platform_image, (deep_length, deep_width))  
platform_image_deep_mid = pygame.transform.scale(platform_image, (deep_length_mid, deep_width))  
platforms = [platform_1, platform_2, platform_3, platform_4, platform_5,platform_6]

#snake
snake_start_x, snake_start_y = 300, 250
snake_width, snake_height = 100, 200
snake = pygame.Rect(snake_start_x, snake_start_y, snake_width, snake_height) 

snake = pygame.image.load('snake.png').convert_alpha()
snake = pygame.transform.scale(snake, (snake_width, snake_height))

# Mängija
player_start_x, player_start_y = 700, 200
player_width, player_height = 100, 100
player = pygame.Rect(player_start_x, player_start_y, player_width, player_height)  # Mängija alguspunkt

#Mängija pildid
player_image_r1 = pygame.image.load('player_RW1.png').convert_alpha()
player_image_r1 = pygame.transform.scale(player_image_r1, (player_width, player_height))

player_image_r2 = pygame.image.load('player_RW2.png').convert_alpha()
player_image_r2 = pygame.transform.scale(player_image_r2, (player_width, player_height))

player_image_l1 = pygame.image.load('player_LW1.png').convert_alpha()
player_image_l1 = pygame.transform.scale(player_image_l1, (player_width, player_height))

player_image_l2 = pygame.image.load('player_LW2.png').convert_alpha()
player_image_l2 = pygame.transform.scale(player_image_l2, (player_width, player_height))

current_image = player_image_r1
animation_time = 200  # Aeg mille tagant ta animatsiooni vahetab
last_update_time = 0
frame = 0

# Kas mängija hetkel liigub kuhugi
moving_r = False
moving_l = False


# Taust
background_image = pygame.image.load('background.jpg')
background_image  = pygame.transform.scale(background_image, (screen_width, screen_height))  # Muuda pildi suurust
 
# Mängija atribuudid
speed = 7 
playerfalling = 0 
gravity = 0.2 
jump = -22  

# Paus ja run
paused = False
run = True

# kuulid ja kuuli klass
bullet_speed = 10
bullets = []

#skoori ja taimeri font preset
skoorifont = pygame.font.SysFont('Arial', 40)

# Mängu kestvus ja skoor
game_time = 60
start_time = time.time()
score = 0

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, shooting_direction):
        super().__init__()
        self.image = pygame.Surface((20, 10))  # Kuuli suurus
        self.image.fill((255,0, 0)) 
        self.rect = self.image.get_rect()
        if shooting_direction == -1:
            self.rect.center = (x-player_width, y)
        else:
            self.rect.center = (x, y)
        self.speed = bullet_speed
        self.shooting_direction = shooting_direction

    def update(self):
        #kuuli liikumine
        self.rect.x += self.speed*self.shooting_direction 

        # Kui kuul on ekraanilt välja, siis kustutab selle
        if self.rect.x > screen_width or self.rect.x < 0 :
            self.kill()
        
def f_end():
    font = pygame.font.SysFont('Arial', 60)
    text = font.render(f'Su lõplik skoor oli: {score}', True, (0, 0, 0))

    #Teksti ekraani keskele (see suht hea, universaalne erinevatele screen suurustele)
    text_width, text_height = text.get_size()
    x_pos = (screen_width - text_width) // 2
    y_pos = (screen_height - text_height) // 2
    screen.blit(text, (x_pos, y_pos))

    # Restart tekst
    font_small = pygame.font.SysFont('Arial', 40)
    small_text = font_small.render('Vajuta Q, et lahkuda mängust.', True, (0, 0, 0))
    screen.blit(small_text, (x_pos, y_pos + 60))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False

platform_coords = [(700, 630), (200, 430), (1200, 430), (250, 10), (1200, 10)]

snake_pos = None
snake_visible = False

#snake spawn
def f_snake():
    global snake_pos, snake_visible
    snake_pos = random.choice(platform_coords)
    snake_visible = True

f_snake()

def pause():
    # Pausi menüü teade
    font = pygame.font.SysFont('Arial', 40)
    text = font.render('Mäng on pausil. Vajuta P tähte, et jätkata.', True, (0, 0, 0))

    #Teksti ekraani keskele (see suht hea, universaalne erinevatele screen suurustele)
    text_width, text_height = text.get_size()
    x_pos = (screen_width - text_width) // 2
    y_pos = (screen_height - text_height) // 2
    screen.blit(text, (x_pos, y_pos))

    # Quit tekst
    font_small = pygame.font.SysFont('Arial', 30)
    small_text = font_small.render('Vajuta Q, et lahkuda.', True, (255, 255, 255))
    screen.blit(small_text, (x_pos, y_pos + 60))

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_p:
                    return True

def respawn():
    global playerfalling
    player.x = player_start_x
    player.y = player_start_y
    playerfalling = 0 
    return True
            
while run:
    screen.fill(color='black')
    screen.blit(background_image, (0,0))
    current_time = pygame.time.get_ticks()
    
    # platforms
    for i in range(len(platforms)):
        if i == 0:
            screen.blit(platform_image_deep_mid, platforms[i])
        elif i == 1 or i == 2:
            screen.blit(platform_image_deep, platforms[i])
        elif i == 3 or i == 4:
            screen.blit(platform_image, platforms[i])
        else:
            screen.blit(platform_image_small, platforms[i])

    screen.blit(current_image, (player.x, player.y))

    if current_time - last_update_time > animation_time:

            if moving_r == True:
                last_update_time = current_time 
                if frame == 0:
                    current_image = player_image_r1
                    frame = 1
                elif frame == 1:
                    current_image = player_image_r2
                    frame = 0
                    
            if moving_l == True:
                last_update_time = current_time 
                if frame == 0:
                        current_image = player_image_l1
                        frame = 1
                elif frame == 1:
                    current_image = player_image_l2
                    frame = 0

    player.y += playerfalling
    
    #Mänguaja arvutamine
    elapsed_time = time.time() - start_time
    remaining_time = max(0, game_time - int(elapsed_time))

    #timeri ja skoori joonistamine
    BLACK = (0,0,0)
    timer_text = skoorifont.render(f"Aega järel: {remaining_time}s", True, BLACK)
    score_text = skoorifont.render(f"Punktid: {score}", True, BLACK)
    screen.blit(timer_text, (10, 10))
    screen.blit(score_text, (10, 50))

    # Gravitatsioon - kui mängija on platvormil või õhus, siis kukutatakse ta allapoole
    for i in range(len(platforms)):
        if player.colliderect(platforms[i]):
            if player.bottom > platforms[i].top:

                #Mängija ei vaju läbi platform
                if player.bottom < (platforms[i].top +25):
                    playerfalling = 0
                    player.bottom = platforms[i].top +5

                #Ei lase mängijal platform sisse minna (paremalt, vasakult)
                else:
                    if platforms[i].left < player.x < platforms[i].right:  # parem
                        
                        player.x = platforms[i].right
                    elif player.x + player_width > platforms[i].left:  # vasak
                        player.x = platforms[i].left - player_width
        
        else:
            playerfalling += gravity 


        if player.top > screen_height:
            respawn()

    # Kuulide liikumine
    for bullet in bullets:
        bullet.update()
        screen.blit(bullet.image, bullet.rect)  # Joonistame iga kuuli

    if snake_visible and snake_pos:
        # Ussi joonistamine
        snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], snake_width, snake_height)
        screen.blit(snake, snake_rect)

    #kuulid vs ussid
    for bullet in bullets:
        if snake_visible and snake_pos:
            snake_rect = pygame.Rect(snake_pos[0], snake_pos[1], snake_width, snake_height)
            if bullet.rect.colliderect(snake_rect):  # Kui kuul tabab koletist
                bullets.remove(bullet)  
                snake_visible = False  
                score += 1  
                pygame.time.set_timer(pygame.USEREVENT, 200) 
                break

    # Nupud
    keys = pygame.key.get_pressed()

    if keys[pygame.K_a]:
        player.move_ip(-speed, 0)
        shooting_direction = -1

        
    if keys[pygame.K_d]:
        player.move_ip(speed, 0)
        shooting_direction = 1

        
    if keys[pygame.K_w]:
        for platform in platforms:
            if player.colliderect(platform):  # Hüpe toimub ainult, kui mängija on platvormil
                if player.bottom >= platform.top:
                    if player.bottom < (platform.top +10):
                        playerfalling = jump
                        

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:  # Paus
                if pause() == False:
                    run = False

            if event.key == pygame.K_a:
                moving_l = True

            if event.key == pygame.K_d:
                moving_r = True

            # Tulistamine
            if event.key == pygame.K_SPACE:  
                #Loodud kuul liikumise suundadega, kui tal pole väärtust, tulistab paremale
                try:
                    shooting_direction = shooting_direction
                except:
                    shooting_direction = 1
                bullet = Bullet(player.x + player_width, player.y + player_height // 2, shooting_direction)
                bullets.append(bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_l = False

            if event.key == pygame.K_d:
                moving_r = False

        if event.type == pygame.USEREVENT:  # Kui taimer käivitub
                f_snake()  # Genereerime uue koletise
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Lülitame taimeri välja

    if remaining_time <= 0:
        if f_end() == False:
            break
    pygame.display.update()

    clock.tick(fps)
pygame.quit()