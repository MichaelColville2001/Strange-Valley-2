import pygame
from variables import variables
from items import items
from inv import Close_Inv,Tab_Switch,Hotbar_Quick_Change
from get_cs import Get_Chunk,Get_Square,Check_If_Block_Cord
from stuff import Get_Line_Angle
from crafting import Get_Assemble_Items,Get_Carve_Items
from use_hand import Use_Clicked,Use_Pressed_Down
from move_player import Move_Player

def Get_Keyboard_Events_Single_Player_Mode(map,itemMap,activeMap,sec,tick,num,mP):
    speed = 10
    tickSpeed = 10
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          variables["running"] = False

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LSHIFT:
            variables["shift"] = True
          if event.key == pygame.K_w:
            variables["w"] = True
          if event.key == pygame.K_a:
            variables["a"] = True
          if event.key == pygame.K_s:
            variables["s"] = True
          if event.key == pygame.K_d:
            variables["d"] = True
          if event.key == pygame.K_TAB and variables["invOn"]: ### TAB
             variables["invOn"] = False
             variables["player"]["objectOpen"] = [None,None]
             Close_Inv(sec,itemMap,map)
          elif event.key == pygame.K_TAB and not variables["invOn"]:
             variables["invOn"] = True

          if event.key == pygame.K_e and not variables["invOn"]: ### TAB
            if Check_If_Block_Cord(map,[variables["player"]["position"][0]+variables["viewCord"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][0],variables["player"]["position"][1]+variables["viewCord"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][1]]):
              object = map[Get_Chunk(variables["player"]["position"][0]+variables["viewCord"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][0],variables["player"]["position"][1]+variables["viewCord"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["position"][0]+variables["viewCord"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][0],variables["player"]["position"][1]+variables["viewCord"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][1],32)]["baseBlock"]
              if object["type"] == "storage" or object["type"] == "foodCooker":
                variables["player"]["objectOpen"] = [variables["player"]["position"][0]+variables["viewCord"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][0],variables["player"]["position"][1]+variables["viewCord"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][1]]
                variables["invOn"] = True
          elif event.key == pygame.K_e and variables["invOn"]: 
              if not variables["player"]["objectOpen"][0] == None:
                variables["player"]["objectOpen"] = [None,None]
                variables["invOn"] = False

          if event.key == pygame.K_1 and not variables["invOn"]: 
             Hotbar_Quick_Change(0,16)
          if event.key == pygame.K_2 and not variables["invOn"]:
             Hotbar_Quick_Change(1,16)
          if event.key == pygame.K_3 and not variables["invOn"]:
             Hotbar_Quick_Change(2,17)
          if event.key == pygame.K_4 and not variables["invOn"]:
             Hotbar_Quick_Change(3,17)

        if event.type == pygame.MOUSEBUTTONDOWN and variables["mouseState"] == "up": ### TAB
          variables["mouseState"] = 'down'
          variables["leftRightMouseButton"] = pygame.mouse.get_pressed()

          if variables["invOn"]:
            if variables["player"][23]["baseInfo"]["type"] == None:
              Get_Assemble_Items(mP)
            elif variables["player"][23]["second"] == "knife":
              Get_Carve_Items(mP) 
            Tab_Switch(num,0,mP,itemMap,sec,variables["shift"],map)

          else:
            Use_Clicked(map,activeMap,itemMap,sec,16)
            Use_Clicked(map,activeMap,itemMap,sec,17)

        if event.type == pygame.MOUSEBUTTONUP and variables["mouseState"] == "down":
            variables["mouseState"] = 'up'
            if variables["invOn"] and not variables["player"]["heldInvObject"]["item"] == items["none"]:
              Tab_Switch(num,1,mP,itemMap,sec,variables["shift"],map)
              
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LSHIFT:
            variables["shift"] = False
          if event.key == pygame.K_w:
            variables["w"] = False
          if event.key == pygame.K_a:
            variables["a"] = False
          if event.key == pygame.K_s:
            variables["s"] = False
          if event.key == pygame.K_d:
            variables["d"] = False

    if variables["shift"]:
      tickSpeed = 7

    if tick % tickSpeed == 0 and not variables["invOn"]:
      Move_Player(map,speed)

    if variables["mouseState"] == "down":
      variables["leftRightMouseButton"] = pygame.mouse.get_pressed()
      Use_Pressed_Down(mP,tick,map,activeMap,itemMap,sec,16)
      Use_Pressed_Down(mP,tick,map,activeMap,itemMap,sec,17)
              
    variables["relativePerspective"][0] = variables["player"]["position"][0]*64-928
    variables["relativePerspective"][1] = variables["player"]["position"][1]*64-508  