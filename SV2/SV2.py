from init import *

from variables import variables
from stuff import Get_Sprite,LO

from single_player import Single_Player_Mode


while variables["running"]:

    Win.fill((0,0,0))

    mP = [0,0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          variables["running"] = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            variables["running"] = False
        if event.type == pygame.MOUSEBUTTONDOWN and variables["mouseState"] == "up":
            variables["mouseState"] = 'down'
        if variables["mouseState"] == "down":
            mP = pygame.mouse.get_pos()
            variables["mouseState"] = "down"
        if event.type == pygame.MOUSEBUTTONUP:
            variables["mouseState"] = 'up'

    Win.blit(Get_Sprite(LO("menu/singlePlayerBanner"),(0,0,0),800),(200,400))
    if mP[0] >= 200 and mP[0] <= 1000 and mP[1] >= 400 and mP[1] <= 600:
      Single_Player_Mode()

    pygame.display.update()