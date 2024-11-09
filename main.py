#Põhi tehtud pygame tutoriali alusel: https://www.youtube.com/watch?v=y9VG3Pztok8&t=445s
# W, A, S, D nupud liikumiseks

import pygame

pygame.init()

screen_width =  800
screen_height = 600

screen = pygame.display.set_mode((screen_width, screen_height))

player = pygame.Rect((300, 250, 50, 50))

run = True
while run:

    #Tekitab tausta, (ilma selleta tekitab mängija enda järele "raja", sest tausta "ei värskendata" ja mängija kujutis joonistatakse ekraanil kõige pealmisele kihile)
    screen.fill(color= 'black')

    #Joonistab ekraanile mängija (kuhu joonistad, RGB värv, mõõtmed)
    pygame.draw.rect(screen, (255, 0, 0), player)

    #Nupuvajutused
    key = pygame.key.get_pressed()
    if key[pygame.K_a] == True:
        player.move_ip(-1, 0)
    elif key[pygame.K_d] == True:
        player.move_ip(1, 0)
    elif key[pygame.K_w] == True:
        player.move_ip(0, -1)
    elif key[pygame.K_s] == True:
        player.move_ip(0, 1)

    #Ristist kinni panemine
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()