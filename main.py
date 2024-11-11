"""
Liikumine hetkel vasakule ja paremale + hüppamine. 

Miski pole kivisse raiutud, kustuta ja muuda julgelt, tegin selle lihtsalt harjutamiseks.

Siit edasi nt: ?
respawn(kui sured)
Maailma lajendamine
Vaba liikumine - et liikumine ei peaks olema ekraani sees, vaid mängija saab liikuda ringi
Liikumine teha sujuvamaks
Minu arust võiks teha ekraani(screeni) suuremaks ja jääda kindla suuruse juurde, et selle ümber hakata ehitama
Äkki teha mingi tickrate, saaks jooksutada kindla FPSi peal - oleks vast stabiilsem

"""
# W, A, S, D nupud liikumiseks, P pausile panemiseks
import pygame

pygame.init()


screen_width =  1280
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))

#Objektid
platform = pygame.Rect(0, 400, 1000, 15)  # Platvormi asukoht ja suurus (x, y, length, width)
platform_floor = pygame.Rect(0, 1000, 1280, 15) 

#Mängija
player = pygame.Rect((300, 250, 50, 50)) #Alguspunkt
speed = 1 #Mängija kiiruse koefitsent
playerfalling = 0  # Vertikaalne liikumiskiirus (langev kiirus)
gravity = 0.01  # Gravitatsiooni tugevus
jump = -2 # Hüppe tugevus    

#Paus ja run
paused = False
run = True

def pause():
    # Pausi menüü teade
    font = pygame.font.SysFont('Arial', 40)
    text = font.render('Mäng on pausil. Vajuta P tähte, et jätkata.', True, (255, 255, 255))

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

    #Mängu sulgemine, pausilt maha võtmine
    #Kuna see on funktsioon peab midagi returnima, et tagasi game loop-i minna
    while True:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                if event.key == pygame.K_p:
                    return True
            if event.type == pygame.QUIT:
                run = False
            

#PÕHITSÜKKEL ehk game loop - väga tähtis :)
while run:
    screen.fill(color='black')

    #Platform
    pygame.draw.rect(screen, (0, 255, 0), platform)
    pygame.draw.rect(screen, (0, 255, 0), platform_floor)

    #Mängija
    pygame.draw.rect(screen, (255, 0, 0), player)
    player.y += playerfalling #Rakendame mängija vertikaalset liikumist
    

    # Gravitatsioon - kui mängija on platvormil või õhus, siis kukutatakse ta allapoole
    if player.colliderect(platform) or player.colliderect(platform_floor) :  # Kui mängija on platvormil
        playerfalling = 0
        player.bottom <= platform.top  # Asetame mängija platvormi peale
    else:
        playerfalling += gravity  # Rakendame gravitatsiooni
    

    # Liikumine:
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        player.move_ip(-speed, 0)
    if keys[pygame.K_d]:
        player.move_ip(speed, 0)
    if keys[pygame.K_w] and player.colliderect(platform):  #Hüpe toimub ainult, kui mängija on platvormil
        playerfalling = jump

    #Eventid
    for event in pygame.event.get():

        if event.type == pygame.QUIT: #Ristist kinni
            run = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_p:#Paus
                if pause() == False:
                     run = False


    pygame.display.update()

pygame.quit()