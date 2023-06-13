import pygame
from pygame.locals import *
from random import *
from time import time
from math import sqrt


pygame.init()
WIDTH, HEIGHT = 1920,1080
Win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Strange Valley 2')

running = True

relativePerspective = [0,0]
mousePosition = [0,0]
tempMousePosition = [0,0]
state = ""

mapChunkSize = [20,20]
invOn = False
 

projectiles = {}

items = {"none":{"type":None,"invSprite":None,"hotbarSprite":None},
         
        "pick":{"type":"hand","first":"tool","second":"pick","damage":10,"durability":100,"invSprite":pygame.image.load("SV2/sprites/invView/pickIV.png").convert_alpha(),"hotbarSprite":pygame.image.load("SV2/sprites/hotbarView/pickHBV.png").convert_alpha()},

        "rock":{"type":"inv","invSprite":pygame.image.load("SV2/sprites/invView/rockIV.png").convert_alpha(),"hotbarSprite":pygame.image.load("SV2/sprites/hotbarView/rockHBV.png").convert_alpha()},

        "helm":{"type":"helm","invSprite":pygame.image.load("SV2/sprites/invView/helmIV.png").convert_alpha(),"hotbarSprite":pygame.image.load("SV2/sprites/hotbarView/helmHBV.png").convert_alpha()}}

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

def Pick_Loot(list):
  item = list[(randint(1,len(list))-1)]
  if item["type"] == None:
    return item
  elif item["type"] == "inv":
    return item
  elif item["type"] == "hand":
    if item["first"] == "tool":
      if item["second"] == "pick":
        return {"type":"hand","first":"tool","second":"pick","durability":item["durability"],"damage":item["damage"],"invSprite":item["invSprite"],"hotbarSprite":item["hotbarSprite"]}
      elif item["second"] == "axe":
        return {"type":"hand","first":"tool","second":"axe","durability":item["durability"],"damage":item["damage"],"invSprite":item["invSprite"],"hotbarSprite":item["hotbarSprite"]}


creatures = {}

floorBlocks = {"grass": {"type":"grass","sprite":pygame.image.load("SV2/sprites/floorBlocks/grass.png").convert_alpha()},
               "dirt": {"sprite":pygame.image.load("SV2/sprites/floorBlocks/dirt.png").convert_alpha()}}

baseBlocks = {"none":{"type":None,"sprite":None},
              "rock":{"type":"rock","sprite":pygame.image.load("SV2/sprites/baseBlocks/rock.png").convert_alpha(),"hp":100,"resistance":0.95,"dropTable":[Drop_Table(items["rock"],1),1]}}

roofBlocks = {"none":{"sprite":None},
              "leaf":{"sprite":pygame.image.load("SV2/sprites/roofBlocks/leaf.png").convert_alpha(),"hp":100,"resistance":0.95,"dropTable":[]}}

activeBlocks = {"none":{"sprite":None}}

interactiveBlocks = {}


heldInvObject = {"item":items["none"],"index":None}

player = {"position": [200,200],
          "sprite":pygame.image.load("SV2/sprites/player/player.png").convert_alpha(),
          "hp":[1,100],
          "mana":[1,100],
          "stam":[1,100],

          "rightHand":items["none"],
          "leftHand":items["none"],

          "helm":items["none"],
          "chest":items["none"],
          "legs":items["none"],
          "boots":items["none"],
          "gloves":items["none"],

          "inventory":[items["pick"],
                       items["helm"],
                       items["rock"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"],
                       items["none"]]}


def Get_Sprite(sheet,colour,spriteSize):
    sprite = pygame.Surface((spriteSize,spriteSize))
    sprite.blit(sheet,(0,0),(0,0,spriteSize,spriteSize))
    sprite = pygame.transform.scale(sprite, (spriteSize, spriteSize))
    sprite.set_colorkey(colour)
    return sprite

def Dis(x1, y1, x2, y2):
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


def Get_Chunk(xPos,yPos,mapChunkX,chunkSize):
    chunkX = int(xPos//chunkSize) 
    chunkY = int(yPos//chunkSize)
    return chunkY*mapChunkX+chunkX

def Get_Square(xPos,yPos,chunkSize):
    x = int(xPos-(xPos//chunkSize)*chunkSize)
    y = int(yPos-(yPos//chunkSize)*chunkSize)
    return (chunkSize*(y+1))-(chunkSize-x)

def Get_Chunk_Clicked(mapChunkSizeX,chunkSize,posClickedX,posClickedY):
   x = ((posClickedX - 928)//64)+player["position"][0]
   y = ((posClickedY - 508)//64)+player["position"][1]
   return Get_Chunk(x,y,mapChunkSizeX,chunkSize)

def Get_Square_Clicked(chunkSize,posClickedX,posClickedY):
   x = ((posClickedX - 928)//64)+player["position"][0]
   y = ((posClickedY - 508)//64)+player["position"][1]
   return Get_Square(x,y,chunkSize)


def Make_Chunks(ChunkSizeX,ChunkSizeY):
    map = []
    for y in range(ChunkSizeY):
      for x in range(ChunkSizeX):
        chunk = []
        for yBlock in range(32):
          for xBlock in range(32):

            floor = {"type":floorBlocks["grass"]["type"],"sprite":floorBlocks["grass"]["sprite"]}
            base = baseBlocks["none"]
            roof = roofBlocks["none"]
            active = activeBlocks["none"]
            if randint(0,25) == 1:
              base = {"type":baseBlocks["rock"]["type"],"sprite":baseBlocks["rock"]["sprite"],"hp":baseBlocks["rock"]["hp"],"resistance":baseBlocks["rock"]["resistance"],"dropTable":baseBlocks["rock"]["dropTable"]}

            chunk.append({"blockPosition":[xBlock+(x*32),yBlock+(y*32)],"floorBlock":floor,"baseBlock":base,"roofBlock":roof,"activeBlock":active})
        map.append({"chunkPosition":[x,y],"chunk":chunk})
    return map

def Make_Item_Chunks(ChunkSizeX,ChunkSizeY):
    itemMap = []
    for y in range(ChunkSizeY):
      for x in range(ChunkSizeX):
        chunk = []
        itemMap.append({"chunkPosition":[x,y],"chunk":chunk})
    return itemMap

def Make_Projectile_Chunks(ChunkSizeX,ChunkSizeY):
    projectileMap = []
    for y in range(ChunkSizeY):
      for x in range(ChunkSizeX):
        chunk = []
        projectileMap.append({"chunkPosition":[x,y],"chunk":chunk})
    return projectileMap


def Hotbar_Quick_Change(num,hand):
    if player["inventory"][num]["type"] == "hand" or player["inventory"][num]["type"] == None:
      temp = player["inventory"][num]
      player["inventory"][num] = player[hand]
      player[hand] = temp
  
def Get_Inv_Item(LX,RX,TY,BY,mP):
   if mP[0] > LX and mP[0] < RX and mP[1] > TY and mP[1] < BY:
      return True
   else:
      return False

def Get_All_Inv_Items(mP):
    num = None
    if Get_Inv_Item(684,822,264,392,mP):
      num = 0 
    elif Get_Inv_Item(822,960,264,392,mP):
      num = 1
    elif Get_Inv_Item(960,1098,264,392,mP):
      num = 2 
    elif Get_Inv_Item(1098,1236,264,392,mP):
      num = 3 
    elif Get_Inv_Item(684,822,402,540,mP):
      num = 4 
    elif Get_Inv_Item(822,960,402,540,mP):
      num = 5
    elif Get_Inv_Item(960,1098,402,540,mP):
      num = 6
    elif Get_Inv_Item(1098,1236,402,540,mP):
      num = 7
    elif Get_Inv_Item(684,822,540,678,mP):
      num = 8
    elif Get_Inv_Item(822,960,540,678,mP):
      num = 9
    elif Get_Inv_Item(960,1098,540,678,mP):
      num = 10
    elif Get_Inv_Item(1098,1236,540,678,mP):
      num = 11
    elif Get_Inv_Item(684,822,678,816,mP):
      num = 12
    elif Get_Inv_Item(822,960,678,816,mP):
      num = 13
    elif Get_Inv_Item(960,1098,678,816,mP):
      num = 14
    elif Get_Inv_Item(1098,1236,678,816,mP):
      num = 15
    elif Get_Inv_Item(753,891,100,238,mP): # Left Hand
      num = 16
    elif Get_Inv_Item(1029,1167,100,238,mP): # Right Hand
      num = 17
    elif Get_Inv_Item(509,647,850,988,mP): # Helm
      num = 18
    elif Get_Inv_Item(700,838,850,988,mP): # Chest
      num = 19
    elif Get_Inv_Item(891,1029,850,988,mP):
      num = 20
    elif Get_Inv_Item(1082,1220,850,988,mP):
      num = 21
    elif Get_Inv_Item(1273,1411,850,988,mP):
      num = 22
    if isinstance(num,int): 
      return num

def Destroy_Item(sec,itemMap):
    for chunk in range(len(itemMap)):
      for item in range(len(itemMap[chunk-1]["chunk"])):
        if itemMap[chunk-1]["chunk"][item-1]["timeLeft"] == sec:
           itemMap[chunk-1]["chunk"].pop(item-1)

def Drop_Item(mousePos,itemMap,item,sec):
    if not item["type"] == None: 
      posX = relativePerspective[0]+mousePos[0]-16
      posY = relativePerspective[1]+mousePos[1]-16
      heldInvObject["item"] = items["none"]
      newMap = itemMap[Get_Chunk(int(posX/64),int(posY/64),mapChunkSize[0],32)]["chunk"].append({"position":[posX,posY],"timeLeft":sec+300,"item":item})
      return newMap

def Put_Back():
    if heldInvObject["index"] < 16:
      player["inventory"][heldInvObject["index"]] = heldInvObject["item"]
      heldInvObject["item"] = items["none"]
    elif heldInvObject["index"] == 16: 
      player["leftHand"] = heldInvObject["item"]
      heldInvObject["item"] = items["none"]
    elif heldInvObject["index"] == 17: 
      player["rightHand"] = heldInvObject["item"]
      heldInvObject["item"] = items["none"]
    elif heldInvObject["index"] == 18: 
      player["helm"] = heldInvObject["item"]
      heldInvObject["item"] = items["none"]
    elif heldInvObject["index"] == 19: 
      player["chest"] = heldInvObject["item"]
      heldInvObject["item"] = items["none"]
    elif heldInvObject["index"] == 20: 
      player["legs"] = heldInvObject["item"]
      heldInvObject["item"] = items["none"]
    elif heldInvObject["index"] == 21: 
      player["boots"] = heldInvObject["item"]
      heldInvObject["item"] = items["none"]
    elif heldInvObject["index"] == 22: 
      player["gloves"] = heldInvObject["item"]
      heldInvObject["item"] = items["none"]


def Tab_Switch(num,type,mP,itemMap,sec):
  if type == 0:
      if isinstance(num,int):
          if num < 16:
            heldInvObject["item"] = player["inventory"][num] 
            player["inventory"][num] = items["none"]
            heldInvObject["index"] = num
          elif num == 16:
            heldInvObject["item"] = player["leftHand"] 
            player["leftHand"] = items["none"]
            heldInvObject["index"] = num
          elif num == 17:
            heldInvObject["item"] = player["rightHand"] 
            player["rightHand"] = items["none"]
            heldInvObject["index"] = num
          elif num == 18:
            heldInvObject["item"] = player["helm"] 
            player["helm"] = items["none"]
            heldInvObject["index"] = num
          elif num == 19:
            heldInvObject["item"] = player["chest"] 
            player["chest"] = items["none"]
            heldInvObject["index"] = num
          elif num == 20:
            heldInvObject["item"] = player["legs"] 
            player["legs"] = items["none"]
            heldInvObject["index"] = num
          elif num == 21:
            heldInvObject["item"] = player["boots"] 
            player["boots"] = items["none"]
            heldInvObject["index"] = num
          elif num == 22:
            heldInvObject["item"] = player["gloves"] 
            player["gloves"] = items["none"]
            heldInvObject["index"] = num
  if type == 1:
      if isinstance(num,int):
                if num < 16:
                  if heldInvObject["index"] < 16:
                    if not heldInvObject["item"]["type"] == None:
                      player["inventory"][heldInvObject["index"]] = player["inventory"][num]
                      player["inventory"][num] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else:
                      Put_Back()
                  elif heldInvObject["index"] == 16: 
                    if player["inventory"][num]["type"] == "hand" or player["inventory"][num]["type"] == None:
                      if not heldInvObject["item"]["type"] == None:
                        player["leftHand"] = player["inventory"][num]
                        player["inventory"][num] = heldInvObject["item"]
                        heldInvObject["item"] = items["none"]
                      else: 
                        Put_Back()
                    else: 
                      Put_Back()
                  elif heldInvObject["index"] == 17: 
                    if player["inventory"][num]["type"] == "hand" or player["inventory"][num]["type"] == None:
                      if not heldInvObject["item"]["type"] == None:
                        player["rightHand"] = player["inventory"][num]
                        player["inventory"][num] = heldInvObject["item"]
                        heldInvObject["item"] = items["none"]
                      else: 
                        Put_Back()
                    else: 
                      Put_Back()
                  elif heldInvObject["index"] == 18: 
                    if player["inventory"][num]["type"] == "helm" or player["inventory"][num]["type"] == None:
                      if not heldInvObject["item"]["type"] == None:
                        player["helm"] = player["inventory"][num]
                        player["inventory"][num] = heldInvObject["item"]
                        heldInvObject["item"] = items["none"]
                      else: 
                        Put_Back()
                    else: 
                      Put_Back()
                  elif heldInvObject["index"] == 19: 
                    if player["inventory"][num]["type"] == "chest" or player["inventory"][num]["type"] == None:
                      if not heldInvObject["item"]["type"] == None:
                        player["chest"] = player["inventory"][num]
                        player["inventory"][num] = heldInvObject["item"]
                        heldInvObject["item"] = items["none"]
                      else: 
                        Put_Back()
                    else: 
                      Put_Back()
                  elif heldInvObject["index"] == 20: 
                    if player["inventory"][num]["type"] == "legs" or player["inventory"][num]["type"] == None:
                      if not heldInvObject["item"]["type"] == None:
                        player["legs"] = player["inventory"][num]
                        player["inventory"][num] = heldInvObject["item"]
                        heldInvObject["item"] = items["none"]
                      else: 
                        Put_Back()
                    else: 
                      Put_Back()
                  elif heldInvObject["index"] == 21: 
                    if player["inventory"][num]["type"] == "boots" or player["inventory"][num]["type"] == None:
                      if not heldInvObject["item"]["type"] == None:
                        player["boots"] = player["inventory"][num]
                        player["inventory"][num] = heldInvObject["item"]
                        heldInvObject["item"] = items["none"]
                      else: 
                        Put_Back()
                    else: 
                      Put_Back()
                  elif heldInvObject["index"] == 22: 
                    if player["inventory"][num]["type"] == "gloves" or player["inventory"][num]["type"] == None:
                      if not heldInvObject["item"]["type"] == None:
                        player["gloves"] = player["inventory"][num]
                        player["inventory"][num] = heldInvObject["item"]
                        heldInvObject["item"] = items["none"]
                      else: 
                        Put_Back()
                    else: 
                      Put_Back()
                elif num == 16:
                  if heldInvObject["index"] < 16:
                    if heldInvObject["item"]["type"] == "hand":
                      player["inventory"][heldInvObject["index"]] = player["leftHand"]
                      player["leftHand"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else: 
                      Put_Back()
                  elif heldInvObject["index"] == 17:
                    if not heldInvObject["item"]["type"] == None:
                      player["rightHand"] = player["leftHand"]
                      player["leftHand"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else: 
                      Put_Back()
                  else: 
                    Put_Back()
                elif num == 17:
                  if heldInvObject["index"] < 16:
                    if heldInvObject["item"]["type"] == "hand":
                      player["inventory"][heldInvObject["index"]] = player["rightHand"]
                      player["rightHand"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else: 
                      Put_Back()
                  elif heldInvObject["index"] == 16:
                    if not heldInvObject["item"]["type"] == None:
                      player["leftHand"] = player["rightHand"]
                      player["rightHand"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else:
                      Put_Back()
                  else: 
                    Put_Back()
                elif num == 18:
                  if heldInvObject["index"] < 16:
                    if heldInvObject["item"]["type"] == "helm":
                      player["inventory"][heldInvObject["index"]] = player["helm"]
                      player["helm"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else: 
                      Put_Back()
                  else: 
                      Put_Back()
                elif num == 19:
                  if heldInvObject["index"] < 16:
                    if heldInvObject["item"]["type"] == "chest":
                      player["inventory"][heldInvObject["index"]] = player["chest"]
                      player["chest"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else: 
                      Put_Back()
                  else: 
                      Put_Back()
                elif num == 20:
                  if heldInvObject["index"] < 16:
                    if heldInvObject["item"]["type"] == "legs":
                      player["inventory"][heldInvObject["index"]] = player["legs"]
                      player["legs"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else: 
                      Put_Back()
                  else: 
                      Put_Back()
                elif num == 21:
                  if heldInvObject["index"] < 16:
                    if heldInvObject["item"]["type"] == "boots":
                      player["inventory"][heldInvObject["index"]] = player["boots"]
                      player["boots"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else: 
                      Put_Back()
                  else: 
                      Put_Back()
                elif num == 22:
                  if heldInvObject["index"] < 16:
                    if heldInvObject["item"]["type"] == "gloves":
                      player["inventory"][heldInvObject["index"]] = player["gloves"]
                      player["gloves"] = heldInvObject["item"]
                      heldInvObject["item"] = items["none"]
                    else: 
                      Put_Back()
                  else: 
                      Put_Back()
      else: 
        if not heldInvObject["item"]["type"] == None:
          itemMap = Drop_Item(mP,itemMap,heldInvObject["item"],sec)


def Get_Keyboard_Events_Editor_Mode():
    global running
    global mousePosition
    global tempMousePosition
    global relativePerspective
    global state
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and state == "up":
            tempMousePosition = pygame.mouse.get_pos()
            state = 'down'
        elif state == "down":
            mousePosition = pygame.mouse.get_pos()
            usedPosition = [mousePosition[0],mousePosition[1]]
            usedPosition[0] = mousePosition[0] - tempMousePosition[0]
            usedPosition[1] = mousePosition[1] - tempMousePosition[1]
            relativePerspective[0] = relativePerspective[0] - usedPosition[0]
            relativePerspective[1] = relativePerspective[1] - usedPosition[1]
            tempMousePosition = mousePosition
            state = "down"
        if event.type == pygame.MOUSEBUTTONUP:
            state = 'up'
        
def Get_Keyboard_Events_Single_Player_Mode(map,itemMap,sec):
    global running
    global mousePosition
    global tempMousePosition
    global relativePerspective
    global state
    global invOn
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT:
          running = False

        if event.type == pygame.MOUSEBUTTONDOWN and state == "up": ### TAB
          state = 'down'
          mP = pygame.mouse.get_pos()
          leftRightMouseButton = pygame.mouse.get_pressed()

          if invOn:
            num = Get_All_Inv_Items(mP)
            Tab_Switch(num,0,mP,itemMap,sec)

          elif not invOn:
            if leftRightMouseButton[0]:
              if map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["type"] == "rock":
                if player["leftHand"]["type"] == "hand":
                  if player["leftHand"]["second"] == "pick":
                    player["leftHand"]["durability"] -= 1
                    map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"] -= player["leftHand"]["damage"]*map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["resistance"]
                    if player["leftHand"]["durability"] <= 0:
                      player["leftHand"] = items["none"]
                    if map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"] <= 0:
                      for item in range(map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["dropTable"][1]):
                        Drop_Item(mP,itemMap,Pick_Loot(map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["dropTable"][0]),sec) 
                      map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"] = baseBlocks["none"]
            if leftRightMouseButton[2]:
               if map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["type"] == "rock":
                if player["rightHand"]["type"] == "hand":
                  if player["rightHand"]["second"] == "pick":
                    player["rightHand"]["durability"] -= 1
                    map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"] -= player["rightHand"]["damage"]*map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["resistance"]
                    if player["rightHand"]["durability"] <= 0:
                      player["rightHand"] = items["none"]
                    if map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"] <= 0:
                      for item in range(map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["dropTable"][1]):
                        Drop_Item(mP,itemMap,Pick_Loot(map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["dropTable"][0]),sec) 
                      map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"] = baseBlocks["none"]

                 
        elif state == "down":
          mP = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONUP and state == "down":
            state = 'up'
            mP = pygame.mouse.get_pos()
            if invOn and not heldInvObject["item"] == items["none"]:
              num = Get_All_Inv_Items(mP)
              Tab_Switch(num,1,mP,itemMap,sec)

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False

          if event.key == pygame.K_TAB and invOn: ### TAB
             invOn = False
          elif event.key == pygame.K_TAB and not invOn:
             invOn = True

          if event.key == pygame.K_1 and not invOn: 
             Hotbar_Quick_Change(0,"leftHand")
          if event.key == pygame.K_2 and not invOn:
             Hotbar_Quick_Change(1,"leftHand")
          if event.key == pygame.K_3 and not invOn:
             Hotbar_Quick_Change(2,"rightHand")
          if event.key == pygame.K_4 and not invOn:
             Hotbar_Quick_Change(3,"rightHand")

          if event.key == pygame.K_w and player["position"][1] > 0 and player["stam"][0] > 15:
            if map[Get_Chunk(player["position"][0],player["position"][1]-1,mapChunkSize[0],32)]["chunk"][Get_Square(player["position"][0],player['position'][1]-1,32)]["baseBlock"]["sprite"] == None:
              player["position"][1] -= 1
              player["stam"][0] -= 15
          if event.key == pygame.K_a and player["position"][0] > 0 and player["stam"][0] > 15:
            if map[Get_Chunk(player["position"][0]-1,player["position"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["position"][0]-1,player['position'][1],32)]["baseBlock"]["sprite"] == None:
              player["position"][0] -= 1
              player["stam"][0] -= 15
          if event.key == pygame.K_s and player["position"][1] < mapChunkSize[1]*32-1 and player["stam"][0] > 15:
            if map[Get_Chunk(player["position"][0],player["position"][1]+1,mapChunkSize[0],32)]["chunk"][Get_Square(player["position"][0],player['position'][1]+1,32)]["baseBlock"]["sprite"] == None:
              player["position"][1] += 1
              player["stam"][0] -= 15
          if event.key == pygame.K_d and player["position"][0] < mapChunkSize[0]*32-1 and player["stam"][0] > 15: 
            if map[Get_Chunk(player["position"][0]+1,player["position"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["position"][0]+1,player['position'][1],32)]["baseBlock"]["sprite"] == None:
              player["position"][0] += 1
              player["stam"][0] -= 15
    relativePerspective[0] = player["position"][0]*64-928
    relativePerspective[1] = player["position"][1]*64-508
  

def Draw_Chunk(chunk):
    global floorBlocks
    global baseBlocks
    global roofBlocks
    global relativePerspective
    for block in range(1024):
       if chunk["chunk"][block]["blockPosition"][0]*64-relativePerspective[0] >= -64 and chunk["chunk"][block]["blockPosition"][0]*64-relativePerspective[0] <= WIDTH and chunk["chunk"][block]["blockPosition"][1]*64-relativePerspective[1] >= -64 and chunk["chunk"][block]["blockPosition"][1]*64-relativePerspective[1] <= HEIGHT:
          Win.blit(Get_Sprite(chunk["chunk"][block]["floorBlock"]["sprite"],(0,0,0),64),((chunk["chunk"][block]["blockPosition"][0]*64-relativePerspective[0],chunk["chunk"][block]["blockPosition"][1]*64-relativePerspective[1])))
          if not chunk["chunk"][block]["baseBlock"]["sprite"] == None:
            Win.blit(Get_Sprite(chunk["chunk"][block]["baseBlock"]["sprite"],(0,0,0),64),((chunk["chunk"][block]["blockPosition"][0]*64-relativePerspective[0],chunk["chunk"][block]["blockPosition"][1]*64-relativePerspective[1])))

def Draw_Screen(map):
    for chunk in map:
      relX = ((relativePerspective[0])/2048)
      relY = ((relativePerspective[1])/2048)
      if (chunk["chunkPosition"][0] < relX+1 and chunk["chunkPosition"][0] > relX-1) and (chunk["chunkPosition"][1] < relY+1 and chunk["chunkPosition"][1] > relY-1):
        Draw_Chunk(chunk)

def Item_Pick_Up(chunk,item):
  if Dis(chunk["chunk"][item-1]["position"][0],chunk["chunk"][item-1]["position"][1],player["position"][0]*64,player["position"][1]*64) < 75:
    for run in range(16):
      if player["inventory"][run] == items["none"]:
        print(player["inventory"][run])
        player["inventory"][run] = chunk["chunk"][item-1]["item"]
        chunk["chunk"].pop(item-1)
        break

def Draw_Item_Chunk(chunk):
    global player
    global relativePerspective
    if len(chunk["chunk"]) > 0:
      for item in range(len(chunk["chunk"])):
        if chunk["chunk"][item-1]["position"][0]-relativePerspective[0] >= -32 and chunk["chunk"][item-1]["position"][0]-relativePerspective[0] <= WIDTH and chunk["chunk"][item-1]["position"][1]-relativePerspective[1] >= -32 and chunk["chunk"][item-1]["position"][1]-relativePerspective[1] <= HEIGHT:
          Win.blit(Get_Sprite(chunk["chunk"][item-1]["item"]["hotbarSprite"],(0,0,0),64),((chunk["chunk"][item-1]["position"][0]-relativePerspective[0],chunk["chunk"][item-1]["position"][1]-relativePerspective[1])))
          Item_Pick_Up(chunk,item)
                


def Draw_Screen_Items(map):
    for chunk in map:
      relX = ((relativePerspective[0])/2048)
      relY = ((relativePerspective[1])/2048)
      if (chunk["chunkPosition"][0] < relX+1 and chunk["chunkPosition"][0] > relX-1) and (chunk["chunkPosition"][1] < relY+1 and chunk["chunkPosition"][1] > relY-1):

        Draw_Item_Chunk(chunk)    

def Draw_Chunk_Roof(chunk):
    global floorBlocks
    global baseBlocks
    global roofBlocks
    global relativePerspective
    for block in range(1024):
       if chunk["chunk"][block]["blockPosition"][0]*64-relativePerspective[0] >= -64 and chunk["chunk"][block]["blockPosition"][0]*64-relativePerspective[0] <= WIDTH and chunk["chunk"][block]["blockPosition"][1]*64-relativePerspective[1] >= -64 and chunk["chunk"][block]["blockPosition"][1]*64-relativePerspective[1] <= HEIGHT:
        if not chunk["chunk"][block]["roofBlock"]["sprite"] == None:
          Win.blit(Get_Sprite(chunk["chunk"][block]["roofBlock"]["sprite"],(0,0,0),64),((chunk["chunk"][block]["blockPosition"][0]*64-relativePerspective[0],chunk["chunk"][block]["blockPosition"][1]*64-relativePerspective[1])))


def Draw_Screen_Roof(map):
    for chunk in map:
      relX = ((relativePerspective[0])/2048)
      relY = ((relativePerspective[1])/2048)
      if (chunk["chunkPosition"][0] < relX+1 and chunk["chunkPosition"][0] > relX-1) and (chunk["chunkPosition"][1] < relY+1 and chunk["chunkPosition"][1] > relY-1):
        Draw_Chunk_Roof(chunk)


def Draw_Inv():
    Win.blit(Get_Sprite(pygame.image.load("SV2/sprites/playerStuff/inv.png").convert_alpha(),(0,0,0),552),(684,264))
    for item in range(16):
        if not player["inventory"][item]["type"] == None: 
          Win.blit(Get_Sprite(player["inventory"][item]["invSprite"],(0,0,0),128),[(item%4*138)+689,(item//4*138)+269])

def Draw_Hotbar():
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/hotbar.png").convert_alpha(),(0,0,0),1068),(426,21))
    if not player["inventory"][0]["hotbarSprite"] == None:
       Win.blit(Get_Sprite(player["inventory"][0]["hotbarSprite"],(0,0,0),32),(432,26))
    if not player["inventory"][1]["hotbarSprite"] == None:
       Win.blit(Get_Sprite(player["inventory"][1]["hotbarSprite"],(0,0,0),32),(582,26))
    if not player["inventory"][2]["hotbarSprite"] == None:
       Win.blit(Get_Sprite(player["inventory"][2]["hotbarSprite"],(0,0,0),32),(1305,26))
    if not player["inventory"][3]["hotbarSprite"] == None:
       Win.blit(Get_Sprite(player["inventory"][3]["hotbarSprite"],(0,0,0),32),(1456,26))

def Draw_Stats():
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/manaStatBar.png").convert_alpha(),(0,0,0),170),(683,21))
    width = int((player["mana"][0]/player["mana"][1])*170)
    pygame.draw.polygon(Win,(0,43,146),[(768-width//2,20),(768+width//2,20),(768+width//2,62),(768-width//2,62)])
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/hpStatBar.png").convert_alpha(),(0,0,0),170),(875,21))
    width = int((player["hp"][0]/player["hp"][1])*170)
    pygame.draw.polygon(Win,(148,0,0),[(960-width//2,20),(960+width//2,20),(960+width//2,62),(960-width//2,62)])
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/stamStatBar.png").convert_alpha(),(0,0,0),170),(1067,21))
    width = int((player["stam"][0]/player["stam"][1])*170)
    pygame.draw.polygon(Win,(190,189,0),[(1152-width//2,20),(1152+width//2,20),(1152+width//2,62),(1152-width//2,62)])

def Draw_Hands():
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/handSlot.png").convert_alpha(),(0,0,0),42),(502,43))
    if not player["leftHand"]["type"] == None:
       Win.blit(Get_Sprite(player["leftHand"]["hotbarSprite"],(0,0,0),32),(507,48))
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/handSlot.png").convert_alpha(),(0,0,0),42),(1378,43))
    if not player["rightHand"]["type"] == None:
       Win.blit(Get_Sprite(player["rightHand"]["hotbarSprite"],(0,0,0),32),(1383,48))
    
def Draw_Equipment():
    Win.blit(Get_Sprite(pygame.image.load("SV2/sprites/playerStuff/invItem.png").convert_alpha(),(0,0,0),138),[753,100]) #LH
    if not player["leftHand"]["type"] == None: 
      Win.blit(Get_Sprite(player["leftHand"]["invSprite"],(0,0,0),128),[758,105])
    Win.blit(Get_Sprite(pygame.image.load("SV2/sprites/playerStuff/invItem.png").convert_alpha(),(0,0,0),138),[1029,100]) #RH
    if not player["rightHand"]["type"] == None:
      Win.blit(Get_Sprite(player["rightHand"]["invSprite"],(0,0,0),128),[1034,105])
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/helm.png").convert_alpha(),(0,0,0),138),(509,850)) #HELM
    if not player["helm"]["type"] == None:
      Win.blit(Get_Sprite(player["helm"]["invSprite"],(0,0,0),128),[514,855])
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/chest.png").convert_alpha(),(0,0,0),138),(700,850)) #Chest
    if not player["chest"]["type"] == None:
      Win.blit(Get_Sprite(player["chest"]["invSprite"],(0,0,0),128),[705,855])
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/legs.png").convert_alpha(),(0,0,0),138),(891,850)) #Legs
    if not player["legs"]["type"] == None:
      Win.blit(Get_Sprite(player["legs"]["invSprite"],(0,0,0),128),[896,855])
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/boots.png").convert_alpha(),(0,0,0),138),(1082,850)) #BOOTS
    if not player["boots"]["type"] == None:
      Win.blit(Get_Sprite(player["boots"]["invSprite"],(0,0,0),128),[1087,855])
    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/playerStuff/gloves.png").convert_alpha(),(0,0,0),138),(1273,850)) #GLOVES
    if not player["gloves"]["type"] == None:
      Win.blit(Get_Sprite(player["gloves"]["invSprite"],(0,0,0),128),[1278,855])

def Draw_Overlay():
    Draw_Hotbar()
    Draw_Hands()

def Draw_Tab():
    Draw_Inv()
    Draw_Equipment()
    if not heldInvObject["item"]["type"] == None:
        xy = pygame.mouse.get_pos()
        Win.blit(Get_Sprite(heldInvObject["item"]["invSprite"],(0,0,0),128),(xy[0]-64,xy[1]-64))


def Change_Player_Stats():
    if player["stam"][0] < player["stam"][1]:
       player["stam"][0] += 1
    if player["hp"][0] < player["hp"][1]:
       player["hp"][0] += .1
    if player["mana"][0] < player["mana"][1]:
       player["mana"][0] += .5


def Editor_Mode():
    map = Make_Chunks(mapChunkSize[0],mapChunkSize[1])
    itemMap = Make_Item_Chunks(mapChunkSize[0],mapChunkSize[1])
    projectileMap = Make_Projectile_Chunks(mapChunkSize[0],mapChunkSize[1])
    while running:
      Win.fill((0,0,0))
      Draw_Screen(map)
      #Draw_Screen_Roof(map)
      Get_Keyboard_Events_Editor_Mode()
      pygame.display.update()

def Single_Player_Mode():
    map = Make_Chunks(mapChunkSize[0],mapChunkSize[1])
    itemMap = Make_Item_Chunks(mapChunkSize[0],mapChunkSize[1])
    projectileMap = Make_Projectile_Chunks(mapChunkSize[0],mapChunkSize[1])
    tick = 0
    sec = 0
    beginSec = time()
    while running:
      Win.fill((0,0,0))

      Draw_Screen(map)
      Draw_Screen_Items(itemMap)
      Win.blit(Get_Sprite(player["sprite"],(0,0,0),64),(928,508))
      #Draw_Screen_Roof(map)

      Get_Keyboard_Events_Single_Player_Mode(map,itemMap,sec)
      Destroy_Item(sec,itemMap)

      Change_Player_Stats()
      Draw_Stats()
      if invOn:
         Draw_Tab()
      else:
         Draw_Overlay()
      tick +=1
      sec = int(time()-beginSec)
      pygame.display.update()
  

while running:

    Win.fill((0,0,0))

    mP = [0,0]

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False
        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_ESCAPE:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN and state == "up":
            state = 'down'
        if state == "down":
            mP = pygame.mouse.get_pos()
            state = "down"
        if event.type == pygame.MOUSEBUTTONUP:
            state = 'up'

    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/menu/sandbox.png").convert_alpha(),(0,0,0),800),(200,100))
    if mP[0] >= 200 and mP[0] <= 1000 and mP[1] >= 100 and mP[1] <= 300:
      Editor_Mode()

    Win.blit(Get_Sprite( pygame.image.load("SV2/sprites/menu/singlePlayerBanner.png").convert_alpha(),(0,0,0),800),(200,400))
    if mP[0] >= 200 and mP[0] <= 1000 and mP[1] >= 400 and mP[1] <= 600:
      Single_Player_Mode()

    pygame.display.update()