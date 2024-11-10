"""
Liikumine hetkel vasakule ja paremale + hüppamine. 
Pausi funktsioon tomib, kuid saaks lühemalt ja kõik ühes kohas.

Miski pole kivisse raiutud, kustuta ja muuda julgelt, tegin selle lihtsalt harjutamiseks.

Siit edasi nt: ?
Maailma lajendamine
Vaba liikumine - et liikumine ei peaks olema ekraani sees, vaid mängija saab liikuda ringi
Liikumine teha sujuvamaks
Minu arust võiks teha ekraani(screeni) suuremaks ja jääda kindla suuruse juurde, et selle ümber hakata ehitama
Äkki teha mingi tickrate, saaks jooksutada kindla FPSi peal - oleks vast stabiilsem

"""
# W, A, S, D nupud liikumiseks, P pausile panemiseks
import pygame

pygame.init()

screen_width =  800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

#Objektid
platform = pygame.Rect(0, 400, 800, 15)  # Platvormi asukoht ja suurus

#Mängija omadused:
player = pygame.Rect((300, 250, 50, 50)) #Alguspunkt
speed = 1 #Mängija kiiruse koefitsent
playerfalling = 0  # Vertikaalne liikumiskiirus (langev kiirus)
gravity = 0.01  # Gravitatsiooni tugevus
jump = -2 # Hüppe tugevus

#Paus ja jooks
paused = False
run = True


#PÕHITSÜKKEL - väga tähtis :)
while run:

    #Ristist kinni panemine ja paus
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused

    if not paused:
        # Tausta värskendamine
        screen.fill(color='black')

        # Gravitatsioon - kui mängija on platvormil või õhus, siis kukutatakse ta allapoole
        if player.colliderect(platform):  # Kui mängija on platvormil
            playerfalling = 0
            player.bottom <= platform.top  # Asetame mängija platvormi peale
        else:
           playerfalling += gravity  # Rakendame gravitatsiooni

        # Liikumine: horisontaalne
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            player.move_ip(-speed, 0)
        if keys[pygame.K_d]:
            player.move_ip(speed, 0)

        # Vertikaalne liikumine: hüpe
        if keys[pygame.K_w] and player.colliderect(platform):  #Hüpe toimub ainult, kui mängija on platvormil
            playerfalling = jump

        # Rakendame mängija vertikaalset liikumist
        player.y += playerfalling

        # Platvormi joonistamine
        pygame.draw.rect(screen, (0, 255, 0), platform)
        # Mängija joonistamine
        pygame.draw.rect(screen, (255, 0, 0), player)

#Mis juhtub kui mäng on pausil
    else:
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
        
        # Kontrollige, kas Q on vajutatud, et mäng sulgeda
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    run = False
        #Unpausing kasutades P tähte
                if event.key == pygame.K_p:
                    paused = not paused
            #Ristist kinni panemine pausi ajal
            if event.type == pygame.QUIT:
                run = False

    pygame.display.update()

pygame.quit()