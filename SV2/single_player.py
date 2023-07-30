import pygame
from draw_overlay import Draw_Stats,Draw_Tab,Draw_Item_Name,Draw_Hotbar
from draw_world import Draw_Screen,Draw_Screen_Items
from key_board_events import Get_Keyboard_Events_Single_Player_Mode
from make_map import Make_Chunks,Make_Basic_Chunks
from player_stats import Change_Player_Stats
from get_num import Get_All_Inv_Items
from variables import variables
from item_stuff import Destroy_Item
from stuff import Get_Sprite,Get_Line_Angle
from time import time
from init import Win
from active_blocks import Tick_Active_Blocks


def Single_Player_Mode():
    map = Make_Chunks(variables["mapChunkSize"][0],variables["mapChunkSize"][1])
    itemMap = Make_Basic_Chunks(variables["mapChunkSize"][0],variables["mapChunkSize"][1])
    #projectileMap = Make_Basic_Chunks(mapChunkSize[0],mapChunkSize[1])
    activeBlockMap = []
    tick = 0
    nextTick = 0
    sec = 0

    while variables["running"]:
      start = time()
      Win.fill((0,0,0))
      xy = pygame.mouse.get_pos()
      num = None
      Draw_Screen(map)
      Draw_Screen_Items(itemMap)
      Win.blit(Get_Sprite(variables["player"]["sprites"][int((Get_Line_Angle([0,0],[xy[0]-960,xy[1]-540])-337.5)//45)],(0,0,0),64),(928,508))
      Tick_Active_Blocks(sec,activeBlockMap,map,itemMap)
      Destroy_Item(sec,itemMap)
      Change_Player_Stats()
      Draw_Stats()
      if variables["invOn"]:
         num = Get_All_Inv_Items(xy,map)
         Draw_Tab(xy,map)
         Draw_Item_Name([xy[0],xy[1]-10],map,num)
      else:
         Draw_Hotbar()
      Get_Keyboard_Events_Single_Player_Mode(map,itemMap,activeBlockMap,sec,tick,num,xy)
      tick +=1
      end = time()
      timeTaken = end-start
      if not int(sec) == int(sec+timeTaken):
        print(tick-nextTick)
        nextTick = tick
      sec += timeTaken
      pygame.display.update()