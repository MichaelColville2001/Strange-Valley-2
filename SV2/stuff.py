import pygame
from math import sqrt,pi
import numpy as np

def LO(name):
  return pygame.image.load("SV2/sprites/"+name+".png").convert_alpha()

def Get_Sprite(sheet,colour,spriteSize):
    sprite = pygame.Surface((spriteSize,spriteSize))
    sprite.blit(sheet,(0,0),(0,0,spriteSize,spriteSize))
    sprite = pygame.transform.scale(sprite, (spriteSize, spriteSize))
    sprite.set_colorkey(colour)
    return sprite

def Drop_Table(*args):
  arg = args
  key_list = arg[::2]
  num_list = arg[1::2]
  weighted_list = []
  interator = 0
  for i in key_list:
    for num in range(num_list[interator]):
      weighted_list.append(i)
    interator += 1
  return weighted_list

def Get_Line_Angle(p1, p2):
    ang1 = np.arctan2(*p1[::-1])
    ang2 = np.arctan2(*p2[::-1])
    return ((ang1 - ang2) % (2 * np.pi))*(180/pi)

def Dist(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

def If_Both_False(ft1,ft2):
    if ft1 and ft2:
      return False
    else:
      return True
    
def Get_Inv_Item_Grid(xy,gridSize,num,mP,size):
    for item in range(gridSize[0]*gridSize[1]):
      if item == size:
         break
      elif mP[0] > (item%gridSize[0]*138)+xy[0] and mP[0] < (item%gridSize[0]*138)+xy[0]+138 and mP[1] > (item//gridSize[0]*138)+xy[1] and mP[1] < (item//gridSize[0]*138)+xy[1]+138:
        return item+num
    else:
      return None
    