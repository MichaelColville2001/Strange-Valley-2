from variables import variables
import pygame
from place_destroy_blocks import Destroy_Block,Place_Block
from items import items

def Use_Hand_Item(mP,hand,LRNum,map,itemMap,activeMap,sec):
  if (LRNum[0] and hand == 16) or (LRNum[2] and hand == 17):
    if variables["player"][hand]["baseInfo"]["type"] == "hand":
      if variables["player"][hand]["first"] == "tool":
        if variables["player"][hand]["second"] == "pick":
          Destroy_Block(mP,hand,map,itemMap,sec,"rock")
        elif variables["player"][hand]["second"] == "axe":
          Destroy_Block(mP,hand,map,itemMap,sec,"wood")
      elif variables["player"][hand]["first"] == "block":
        Place_Block(mP,hand,map,activeMap)
    elif variables["player"][hand] == items["none"]:
      Destroy_Block(mP,hand,map,itemMap,sec,"")

def Use_Pressed_Down(mP,tick,map,activeMap,itemMap,sec,hand):
        if not variables["player"][hand]["speed"] == 0:
          if not variables["invOn"]:
            if tick % variables["player"][hand]["speed"] == 0:
              Use_Hand_Item(mP,hand,variables["leftRightMouseButton"],map,itemMap,activeMap,sec)

def Use_Clicked(map,activeMap,itemMap,sec,hand):
  if not variables["player"][hand] == items["none"]:
    if variables["player"][hand]["speed"] == 0 and variables["player"][hand]["coolDown"] == 0:
      mP = pygame.mouse.get_pos()
      leftRightMouseButton = pygame.mouse.get_pressed()
      if not variables["invOn"]:
          Use_Hand_Item(mP,hand,leftRightMouseButton,map,itemMap,activeMap,sec)