"""
Mängu tegid: Karl-Markus Hannust ja Robert Palm


NB: Mängu käivitamiseks on vaja mängu tausta ja tegelase pildifaile ning pygame moodulit.


Praegu on mäng algfaasis. Mängija saab liikuda, tulistada ning platformid töötavad nagu vaja.
Mängul pole veel eriti sisu, kuid palju põhilisi asju on tehtud.


Nupud:
W, A, S, D -Liikumine
SPACE - tulistamine
P - mängu pausile panemine


Pygamesi baasiks ja õppimiseks kasutasime - 
https://www.youtube.com/watch?v=y9VG3Pztok8

Mängu tegelane on ajutine ja joonistasime ise lehel - 
https://www.pixilart.com/draw

Mängu taust on ajutine ning võtsime lehelt, kus olid litsentsivabad tehisintellekti pildid, kuid lõppversioonis tahame ise oma kunsti luua - 
https://www.freepik.com/free-photos-vectors/pixel-art-cloud

"""
import pygame

pygame.init()

screen_width, screen_height =  1600, 1060
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
fps = 60


# Platvormi asukoht ja suurus (x, y, length, width)
platform_1 = pygame.Rect(100, 500, 400, 40)
platform_2 = pygame.Rect(700, 500, 400, 40)

platformid = [platform_1, platform_2]

# Mängija, taust
player_start_x, player_start_y = 300, 250
player_width, player_height = 100, 100
player = pygame.Rect(player_start_x, player_start_y, player_width, player_height)  # Mängija alguspunkt

player_image = pygame.image.load('player_character.png').convert_alpha()
player_image = pygame.transform.scale(player_image, (player_width, player_height)) 

background_image = pygame.image.load('background.jpg')
background_image  = pygame.transform.scale(background_image, (screen_width, screen_height))  # Muuda pildi suurust
 
# Mängija atribuudid
speed = 7 
playerfalling = 0 
gravity = 0.3 
jump = -6    

# Paus ja run
paused = False
run = True

# kuulid ja kuuli klass
bullet_speed = 10
bullets = []

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
                return
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
    
    # platformid
    pygame.draw.rect(screen, (0, 255, 0), platform_1)
    pygame.draw.rect(screen, (0, 255, 0), platform_2)


    # Mängija
    screen.blit(player_image, (player.x, player.y))

    player.y += playerfalling
    

    # Gravitatsioon - kui mängija on platvormil või õhus, siis kukutatakse ta allapoole
    for i in range(len(platformid)):
        if player.colliderect(platformid[i]):
            if player.bottom >= platformid[i].top:

                #Mängija ei vaju läbi platformi
                if player.bottom < (platformid[i].top +25):
                    playerfalling = 0
                    player.bottom = platformid[i].top +5

                #Ei lase mängijal platformi sisse minna (paremalt, vasakult)
                else:
                    if platformid[i].left < player.x < platformid[i].right:  # parem
                        player.x = platformid[i].right
                    elif player.x + player_width > platformid[i].left:  # vasak
                        player.x = platformid[i].left - player_width
        
        else:
            playerfalling += gravity 


        if player.top > screen_height:
            respawn()

    # Kuulide liikumine
    for bullet in bullets:
        bullet.update()
        screen.blit(bullet.image, bullet.rect)  # Joonistame iga kuuli

    # Nupud
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move_ip(-speed, 0)
        shooting_direction = -1
    if keys[pygame.K_d]:
        player.move_ip(speed, 0)
        shooting_direction = 1 
        
    if keys[pygame.K_w]:
        for platform in platformid:
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
                     
            # Tulistamine
            if event.key == pygame.K_SPACE:  
                # Loodud kuul liikumise suundadega, kui tal pole väärtust, tulistab paremale
                try:
                    shooting_direction = shooting_direction
                except:
                    shooting_direction = 1
                bullet = Bullet(player.x + player_width, player.y + player_height // 2, shooting_direction)
                bullets.append(bullet)

    pygame.display.update()

    clock.tick(fps)
pygame.quit()