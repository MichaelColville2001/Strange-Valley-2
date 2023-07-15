import pygame
from pygame.locals import *
from random import *
import numpy as np
from math import sqrt,pi
from time import time

##################################################################################################################################################################################

pygame.init()
pygame.display.set_caption('Strange Valley 2')
WIDTH, HEIGHT = 1920,1080
Win = pygame.display.set_mode((WIDTH, HEIGHT))

#######################################################################################################################################################################################

running = True

relativePerspective = [0,0]
mousePosition = [0,0]
tempMousePosition = [0,0]
mouseState = ""
leftRightMouseButton = [False,False,False]

mapChunkSize = [25,25] #max 100x100

viewCord = [[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1]]

invOn = False

shift = False
w = False
a = False
s = False
d = False

######################################################################################################################################################################################

def LO(name):
  return pygame.image.load("SV2/sprites/"+name+".png").convert_alpha()

####################################################################################################################################################################################

projectiles = {}

######################################################################################################################################################################################

items = {"none":{"baseInfo":{"name":None,"type":None,"stacks":False,"invSprite":None,"itemSprite":None},"speed":15},
         
        "Camp_Fire":{"baseInfo":{"name":"Camp_Fire","type":"hand","stacks":False,"invSprite":LO("invView/campFire"),"itemSprite":LO("itemSprite/campFire")},"first":"block","second":"active","tier":1,"speed":0,"coolDown":0}, 

        "Fired_Clay_Pot":{"baseInfo":{"name":"Fired_Clay_Pot","type":"hand","stacks":False,"invSprite":LO("invView/firedClayPot"),"itemSprite":LO("itemSprite/firedClayPot")},"first":"block","second":"inActive","tier":1,"speed":0,"coolDown":0},   
        "Wood_Chest":{"baseInfo":{"name":"Wood_Chest","type":"hand","stacks":False,"invSprite":LO("invView/woodChest"),"itemSprite":LO("itemSprite/woodChest")},"first":"block","second":"inActive","tier":2,"speed":0,"coolDown":0},   
        "Reinforced_Wood_Chest":{"baseInfo":{"name":"Reinforced_Wood_Chest","type":"hand","stacks":False,"invSprite":LO("invView/reinforcedWoodChest"),"itemSprite":LO("itemSprite/reinforcedWoodChest")},"first":"block","second":"inActive","tier":3,"speed":0,"coolDown":0},   
        "Iron_Safe":{"baseInfo":{"name":"Iron_Safe","type":"hand","stacks":False,"invSprite":LO("invView/ironSafe"),"itemSprite":LO("itemSprite/ironSafe")},"first":"block","second":"inActive","tier":4,"speed":0,"coolDown":0},   
        "Steel_Safe":{"baseInfo":{"name":"Steel_Safe","type":"hand","stacks":False,"invSprite":LO("invView/steelSafe"),"itemSprite":LO("itemSprite/steelSafe")},"first":"block","second":"inActive","tier":5,"speed":0,"coolDown":0},   

        "Pry_Stick":{"baseInfo":{"name":"Pry_Stick","type":"hand","stacks":False,"invSprite":LO("invView/pryStick"),"itemSprite":LO("itemSprite/pryStick")},"first":"tool","second":"pick","tier":1,"damage":10,"durability":[100,100],"speed":20},
        "Stone_Axe":{"baseInfo":{"name":"Stone_Axe","type":"hand","stacks":False,"invSprite":LO("invView/stoneAxe"),"itemSprite":LO("itemSprite/stoneAxe")},"first":"tool","second":"axe","tier":1,"damage":10,"durability":[100,100],"speed":20},
        "Stone_Knife":{"baseInfo":{"name":"Stone_Knife","type":"hand","stacks":False,"invSprite":LO("invView/stoneKnife"),"itemSprite":LO("itemSprite/stoneKnife")},"first":"tool","second":"knife","tier":1,"durability":[1,1],"damage":10,"speed":0,"coolDown":1},

        "Stone":{"baseInfo":{"name":"Stone","type":"inv","stacks":True,"invSprite":LO("invView/rock"),"itemSprite":LO("itemSprite/rock")},"stack":[5,8]},
        "Wood":{"baseInfo":{"name":"Wood","type":"inv","stacks":True,"invSprite":LO("invView/wood"),"itemSprite":LO("itemSprite/wood")},"stack":[1,8]},
        "Clay":{"baseInfo":{"name":"Clay","type":"inv","stacks":True,"invSprite":LO("invView/clay"),"itemSprite":LO("itemSprite/clay")},"stack":[1,8]},
        "Wood_Axe_Handle":{"baseInfo":{"name":"Wood_Axe_Handle","type":"inv","stacks":True,"invSprite":LO("invView/woodAxeHandle"),"itemSprite":LO("itemSprite/woodAxeHandle")},"stack":[1,8]},

        "Helm":{"baseInfo":{"name":"Helm","type":"helm","stacks":False,"invSprite":LO("invView/helm"),"itemSprite":LO("itemSprite/helm")}}
        }

######################################################################################################################################################################################

assembely ={"Stone_Knife":{"ingredients":[["Stone",2]]},
            "Stone_Axe":{"ingredients":[["Wood_Axe_Handle",1],["Stone_Knife",1]]},
            "Camp_Fire":{"ingredients":[["Stone",8],["Wood",2]]}}

carving = {"Pry_Stick":{"tier":0,"work":1,"ingredients":[["Wood",1]]},
           "Wood_Axe_Handle":{"tier":0,"work":1,"ingredients":[["Wood",1]]}}

#########################################################################################################################################################################################

def Check_For_Item(item,itemAmount):
  total = itemAmount
  item = items[item]
  for num in range(16):
    if player["inventory"][num]["baseInfo"]["name"] == item["baseInfo"]["name"]:
      if item["baseInfo"]["stacks"]:
        total -= player["inventory"][num]["stack"][0]
      else:
        total -= 1
  if total <= 0:
    return True
  else:
    return False
  
def Can_Assemble(craftingItem):
  for items in range(len(assembely[craftingItem]["ingredients"])):
    if not Check_For_Item(assembely[craftingItem]["ingredients"][items][0],assembely[craftingItem]["ingredients"][items][1]):
      return False
  return True

def Can_Carve(craftingItem):
  if player["craftingTool"]["durability"][0] >= carving[craftingItem]["work"] and player["craftingTool"]["tier"] >= carving[craftingItem]["tier"]:
    for items in range(len(carving[craftingItem]["ingredients"])):
      if not Check_For_Item(carving[craftingItem]["ingredients"][items][0],carving[craftingItem]["ingredients"][items][1]):
        return False
    return True
  else:
    return False

def Assemble(craftingItem):
  if player["craftingOutput"]["baseInfo"]["type"] == None:
    if Can_Assemble(craftingItem):
      for objects in range(len(assembely[craftingItem]["ingredients"])):
        item = items[assembely[craftingItem]["ingredients"][objects][0]]
        amount = assembely[craftingItem]["ingredients"][objects][1]
        if item["baseInfo"]["stacks"]:
          for some in range(16):
            if amount == 0:
              break
            if item["baseInfo"]["name"] == player["inventory"][some]["baseInfo"]["name"]:
              if (amount - player["inventory"][some]["stack"][0]) >= 0:
                amount -= player["inventory"][some]["stack"][0]
                player["inventory"][some] = items["none"]
              elif (amount - player["inventory"][some]["stack"][0]) < 0:
                player["inventory"][some]["stack"][0] -= amount
                amount = 0
        else:
          for some in range(16):
            if amount == 0:
              break
            if item["baseInfo"]["name"] == player["inventory"][some]["baseInfo"]["name"]:
                player["inventory"][some] = items["none"]
                amount -= 1
      player["craftingOutput"] = Convert_Item(items[craftingItem])

def Carve(craftingItem):
  if player["craftingOutput"]["baseInfo"]["type"] == None:
    if Can_Carve(craftingItem):
      for objects in range(len(carving[craftingItem]["ingredients"])):
        item = items[carving[craftingItem]["ingredients"][objects][0]]
        amount = carving[craftingItem]["ingredients"][objects][1]
        if item["baseInfo"]["stacks"]:
          for some in range(16):
            if amount == 0:
              break
            if item["baseInfo"]["name"] == player["inventory"][some]["baseInfo"]["name"]:
              if (amount - player["inventory"][some]["stack"][0]) >= 0:
                amount -= player["inventory"][some]["stack"][0]
                player["inventory"][some] = items["none"]
              elif (amount - player["inventory"][some]["stack"][0]) < 0:
                player["inventory"][some]["stack"][0] -= amount
                amount = 0
      player["craftingTool"]["durability"][0] -= carving[craftingItem]["work"]
      if player["craftingTool"]["durability"][0] == 0:
        player["craftingTool"] = items["none"]
      player["craftingOutput"] = Convert_Item(items[craftingItem])

#######################################################################################################################################################################################

def Convert_Item(item):
  type = item["baseInfo"]["type"]
  if type == None:
    return {"baseInfo":{"name":None,"type":None,"stacks":False,"invSprite":None,"itemSprite":None}}
  elif type == "inv":
    if item["baseInfo"]["stacks"]:
      return {"baseInfo":item["baseInfo"],"stack":item["stack"].copy()}
  elif type == "hand":
    if item["first"] == "tool":
      if item["second"] == "pick":
        return {"baseInfo":item["baseInfo"],"first":item["first"],"second":item["second"],"tier":item["tier"],"damage":item["damage"],"durability":[item["durability"][0],item["durability"][1]],"speed":item["speed"]}
      if item["second"] == "axe":
        return {"baseInfo":item["baseInfo"],"first":item["first"],"second":item["second"],"tier":item["tier"],"damage":item["damage"],"durability":[item["durability"][0],item["durability"][1]],"speed":item["speed"]}
      if item["second"] == "knife":
        return {"baseInfo":item["baseInfo"],"first":item["first"],"second":item["second"],"tier":item["tier"],"damage":item["damage"],"durability":[item["durability"][0],item["durability"][1]],"speed":item["speed"],"coolDown":item["coolDown"]}
    elif item["first"] == "block":
      if item["second"] == "active":
        return {"baseInfo":item["baseInfo"],"first":item["first"],"second":item["second"],"tier":item["tier"],"speed":item["speed"],"coolDown":item["coolDown"]}
      if item["second"] == "inActive":
        return {"baseInfo":item["baseInfo"],"first":item["first"],"second":item["second"],"tier":item["tier"],"speed":item["speed"],"coolDown":item["coolDown"]}
  elif type == "helm":
    return {"baseInfo":item["baseInfo"]}
  

def Convert_Blocks(item):
  mP = pygame.mouse.get_pos()
  if item["blockType"] == "floor":
    return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"][randint(0,len(item["sprites"])-1)]} 
  
  if item["blockType"] == "base":
    if item["type"] == None:
      return{"name":None,"blockType":"base","type":None,"sprites":None}
    else:
      return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"][randint(0,len(item["sprites"])-1)],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],"dropTable":item["dropTable"]} 
    
  if item["blockType"] == "plant":
    return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"][randint(0,len(item["sprites"])-1)],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],"dropTable":item["dropTable"]} 

  if item["blockType"] == "pile":
    return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"][randint(0,len(item["sprites"])-1)],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],"dropTable":item["dropTable"]} 

  if item["blockType"] == "inActive":
    if item["type"] == "storage":
      if item["name"] == "Fired_Clay_Pot":
        return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],"inv":[item["inv"][0],item["inv"][1],item["inv"][2],item["inv"][3]]} 
      if item["name"] == "Wood_Chest" or item["name"] == "Reinforced_Wood_Chest":
        return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-315)//90)],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],"inv":[item["inv"][0],item["inv"][1],item["inv"][2],item["inv"][3],item["inv"][4],item["inv"][5],item["inv"][6],item["inv"][7],item["inv"][8]]} 
      if item["name"] == "Iron_Safe" or item["name"] == "Steel_Safe":
        return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-315)//90)],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],"inv":[item["inv"][0],item["inv"][1],item["inv"][2],item["inv"][3],item["inv"][4],item["inv"][5],item["inv"][6],item["inv"][7],item["inv"][8],item["inv"][9],item["inv"][10],item["inv"][11],item["inv"][12],item["inv"][13],item["inv"][14],item["inv"][15]]} 

  if item["blockType"] == "active":
    return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"blockPosition":[item["blockPostion"][0],item["blockPostion"][1]],"active":item["active"],"onSprite":item["onSprite"],"offSprite":item["offSprite"],"cookingInv":item["cookingInv"],"outPutInv":item["outPutInv"],"fuelInv":item["fuelInv"],"dropTable":item["dropTable"],"timeLeft":item["timeLeft"],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"]}

########################################################################################################################################################################################

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
  return Convert_Item(item)

######################################################################################################################################################################################################

creatures = {}

#######################################################################################################################################################################################

floorBlocks = {"Grass": {"name":"Grass","blockType":"floor","type":"grass","sprites":[LO("floorBlocks/grass1"),LO("floorBlocks/grass2"),LO("floorBlocks/grass3"),LO("floorBlocks/grass4")]},
               "Water": {"name":"Water","blockType":"floor","type":"water","sprites":[LO("floorBlocks/water")]},
               "Dirt": {"name":"Dirt","blockType":"floor","type":"dirt","sprites":[LO("floorBlocks/dirt")]}}

# # # # #

baseBlocks = {"none":{"name":None,"blockType":"base","type":None,"sprites":None},
              
              "Rock":{"name":"Rock","blockType":"base","type":"rock","sprites":[LO("baseBlocks/rock")],"tier":2,"hp":[100,100],"resistance":0.95,"dropTable":[Drop_Table(items["Stone"],1),5]},
              "Log":{"name":"Log","blockType":"base","type":"wood","sprites":[LO("baseBlocks/wood")],"tier":1,"hp":[100,100],"resistance":0.95,"dropTable":[Drop_Table(items["Wood"],1),5]},

              "Rock_Pile":{"name":"Rock_Pile","blockType":"pile","type":"rock","sprites":[LO("baseBlocks/rockPile1"),LO("baseBlocks/rockPile2"),LO("baseBlocks/rockPile3"),LO("baseBlocks/rockPile4")],"tier":0,"hp":[100,100],"resistance":1,"dropTable":[Drop_Table(items["Stone"],2,items["none"],1),5]},

              "Bush":{"name":"Bush","blockType":"plant","type":"wood","sprites":[LO("baseBlocks/bush")],"tier":0,"hp":[100,100],"resistance":1,"dropTable":[Drop_Table(items["Wood"],2,items["none"],1),5]},
              
              # # # # #

              "Clay_Brick_Wall":{"name":"Clay_Brick_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":1,"hp":[100,100],"resistance":0.95},
              "Adobe_Wall":{"name":"Adobe_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":1,"hp":[100,100],"resistance":0.95},
              "Wood_Wall":{"name":"Wood_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":2,"hp":[100,100],"resistance":0.95},
              "Reinforced_Wood_Wall":{"name":"Reinforced_Wood_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":3,"hp":[100,100],"resistance":0.95},
              "Stone_Wall":{"name":"Stone_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":4,"hp":[100,100],"resistance":0.95},
              "Reinforced_Concrete_Wall":{"name":"Reinforced_Concrete_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":5,"hp":[100,100],"resistance":0.95},

              # # # # #

              "Fired_Clay_Pot":{"name":"Fired_Clay_Pot","blockType":"inActive","type":"storage","sprites":LO("inActiveBlocks/firedClayPot"),"tier":1,"hp":[100,100],"resistance":0.95,"inv":[Convert_Item(items["Stone"]),items["none"],items["none"],items["none"]]},
              "Wood_Chest":{"name":"Wood_Chest","blockType":"inActive","type":"storage","sprites":[LO("inActiveBlocks/woodChest3"),LO("inActiveBlocks/woodChest4"),LO("inActiveBlocks/woodChest1"),LO("inActiveBlocks/woodChest2")],"tier":2,"hp":[100,100],"resistance":0.95,"inv":[items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],Convert_Item(items["Pry_Stick"]),items["none"],items["none"]]},
              "Reinforced_Wood_Chest":{"name":"Reinforced_Wood_Chest","blockType":"inActive","type":"storage","sprites":[LO("inActiveBlocks/reinforcedWoodChest3"),LO("inActiveBlocks/reinforcedWoodChest4"),LO("inActiveBlocks/reinforcedWoodChest1"),LO("inActiveBlocks/reinforcedWoodChest2")],"tier":3,"hp":[100,100],"resistance":0.95,"inv":[items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"]]},
              "Iron_Safe":{"name":"Iron_Safe","blockType":"inActive","type":"storage","sprites":[LO("inActiveBlocks/ironSafe3"),LO("inActiveBlocks/ironSafe4"),LO("inActiveBlocks/ironSafe1"),LO("inActiveBlocks/ironSafe2")],"tier":4,"hp":[100,100],"resistance":0.95,"inv":[items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"]]},
              "Steel_Safe":{"name":"Steel_Safe","blockType":"inActive","type":"storage","sprites":[LO("inActiveBlocks/steelSafe3"),LO("inActiveBlocks/steelSafe4"),LO("inActiveBlocks/steelSafe1"),LO("inActiveBlocks/steelSafe2")],"tier":5,"hp":[100,100],"resistance":0.95,"inv":[items["none"],items["none"],items["none"],items["none"],items["none"],Convert_Item(items["Pry_Stick"]),items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"]]}}

# # # # #

activeBlocks = {"none":{"type":None,"sprite":None},
                "Camp_Fire":{"name":"Camp_Fire","blockType":"active","type":"foodCooker","blockPostion":[None,None],"active":False,"onSprite":LO("activeBlocks/onCampFire"),"offSprite":LO("activeBlocks/offCampFire"),"cookingInv":[items["none"],items["none"],items["none"]],"outPutInv":[items["none"],items["none"],items["none"]],"fuelInv":[items["none"],items["none"]],"dropTable":[Drop_Table(items["Camp_Fire"],1),1],"timeLeft":0,"tier":0,"hp":[100,100],"resistance":0.95}}

#######################################################################################################################################################################################

player = {"position": [10,10],
          "sprites":[LO("player/player1"),
                     LO("player/player2"),
                     LO("player/player3"),
                     LO("player/player4"),
                     LO("player/player5"),
                     LO("player/player6"),
                     LO("player/player7"),
                     LO("player/player8")],
          "hp":[1,100],
          "mana":[1,100],
          "stam":[1,100],
          "objectOpen":[None,None],
          "heldInvObject":{"item":items["none"],"index":None},
          "craftingTool":items["none"],
          "craftingOutput":items["none"],
          "rightHand":items["none"],
          "leftHand":items["none"],
          "helm":items["none"],
          "chest":items["none"],
          "legs":items["none"],
          "boots":items["none"],
          "gloves":items["none"],
          "inventory":[Convert_Item(items["Fired_Clay_Pot"]),Convert_Item(items["Wood_Chest"]),Convert_Item(items["Steel_Safe"]),items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"],items["none"]]}

########################################################################################################################################################################################

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
    
def Get_Inv_Item(LX,RX,TY,BY,mP):
   if mP[0] > LX and mP[0] < RX and mP[1] > TY and mP[1] < BY:
      return True
   else:
      return False

######################################################################################################################################################################################

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

def Get_Square_Cord(cordClickedX,cordClickedY):
  x = ((cordClickedX - 928)//64)+player["position"][0]
  y = ((cordClickedY - 508)//64)+player["position"][1]
  return [x,y]

########################################################################################################################################################################################

def Get_Chunks_To_Draw(ChunkSizeX,ChunkSizeY,x,y,xBlock,yBlock):
    if (xBlock == 15 or xBlock == 16) and (yBlock >= 8 and yBlock <= 23): 
      return [[x,y]]
    elif (xBlock >= 0 and xBlock <= 14) and (yBlock >= 8 and yBlock <= 23): 
      if x - 1 >= 0:
        return [[x,y],[x-1,y]]
      else:
        return [[x,y]]
    elif (xBlock >= 17 and xBlock <= 31) and (yBlock >= 8 and yBlock <= 23): 
      if x + 1 <= ChunkSizeX-1:
        return [[x,y],[x+1,y]]
      else:
        return [[x,y]]   
    elif (xBlock == 15 or xBlock == 16) and (yBlock >= 0 and yBlock <= 7): 
      if y - 1 >= 0:
        return [[x,y],[x,y-1]]
      else:
        return [[x,y]]   
    elif (xBlock == 15 or xBlock == 16) and (yBlock >= 24 and yBlock <= 31): 
      if y + 1 <= ChunkSizeY:
        return [[x,y],[x,y+1]]
      else:
        return [[x,y]]     
    elif (xBlock >= 0 and xBlock <= 14) and (yBlock >= 0 and yBlock <= 7): 
      if x - 1 >= 0 and y - 1 >= 0:
        return [[x,y],[x-1,y-1],[x-1,y],[x,y-1]]
      elif x - 1 >= 0:
        return [[x,y],[x-1,y]]
      elif y - 1 >= 0:
        return [[x,y],[x,y-1]]
      else:
        return [[x,y]] 
    elif (xBlock >= 17 and xBlock <= 31) and (yBlock >= 0 and yBlock <= 7): 
      if x + 1 <= ChunkSizeX-1 and y - 1 >= 0:
        return [[x,y],[x+1,y-1],[x+1,y],[x,y-1]]
      elif x + 1 <= ChunkSizeX-1:
        return [[x,y],[x+1,y]]
      elif y - 1 >= 0:
        return [[x,y],[x,y-1]]
      else:
        return [[x,y]] 
    elif (xBlock >= 17 and xBlock <= 31) and (yBlock >= 24 and yBlock <= 31):
      if x + 1 <= ChunkSizeX-1 and y + 1 <= ChunkSizeY-1:
        return [[x,y],[x+1,y+1],[x+1,y],[x,y+1]]
      elif x + 1 <= ChunkSizeX-1:
        return [[x,y],[x+1,y]]
      elif y + 1 <= ChunkSizeY-1:
        return [[x,y],[x,y+1]]
      else:
        return [[x,y]] 
    elif (xBlock >= 0 and xBlock <= 14) and (yBlock >= 24 and yBlock <= 31):
      if x - 1 >= 0 and y + 1 <= ChunkSizeY-1:
        return [[x,y],[x-1,y+1],[x-1,y],[x,y+1]]
      elif x - 1 >= 0:
        return [[x,y],[x-1,y]]
      elif y + 1 <= ChunkSizeY-1:
        return [[x,y],[x,y+1]]
      else:
        return [[x,y]]


def Make_Chunks(ChunkSizeX,ChunkSizeY):
    map = []
    for y in range(ChunkSizeY):
      for x in range(ChunkSizeX):
        chunk = []
        for yBlock in range(32):
          for xBlock in range(32):
            floor = Convert_Blocks(floorBlocks["Grass"])
            base = Convert_Blocks(baseBlocks["none"])
            if randint(0,25) == 1:
              base = Convert_Blocks(baseBlocks["Rock"])
            elif randint(0,100) == 1:
              base = Convert_Blocks(baseBlocks["Log"])
            elif randint(0,50) == 1:
              base = Convert_Blocks(baseBlocks["Rock_Pile"])
            elif randint(0,100) == 1:
              base = Convert_Blocks(baseBlocks["Bush"])
            elif randint(0,1000) == 1:
              player["position"][0] = x
              player["position"][1] = y
            chunk.append({"position":[xBlock+(x*32),yBlock+(y*32)],"floorBlock":floor,"baseBlock":base})
        map.append({"chunkPosition":[x,y],"chunk":chunk})
    return map

def Make_Active_Block_Chunks(ChunkSizeX,ChunkSizeY):
    map = []
    for y in range(ChunkSizeY):
      for x in range(ChunkSizeX):
        chunk = []
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

###################################################################################################################################################################################

def Hotbar_Quick_Change(num,hand):
    if player["inventory"][num]["baseInfo"]["type"] == "hand" or player["inventory"][num]["baseInfo"]["type"] == None:
      temp = player["inventory"][num]
      player["inventory"][num] = player[hand]
      player[hand] = temp

####################################################################################################################################################################################
   
def Get_Assemble_Items(mP):
    if Get_Inv_Item(1305,1443,269,407,mP):
      Assemble("Stone_Knife")
    if Get_Inv_Item(1444,1582,269,407,mP):
      Assemble("Stone_Axe")
    if Get_Inv_Item(1583,1721,269,407,mP):
      Assemble("Camp_Fire")

def Get_Carve_Items(mP):
    if Get_Inv_Item(1305,1443,269,407,mP):
      Carve("Pry_Stick")
    if Get_Inv_Item(1444,1582,269,407,mP):
      Carve("Wood_Axe_Handle")

def Get_4_Storage(mP):
    num = None
    if Get_Inv_Item(206,344,402,540,mP):
      num = 25
    elif Get_Inv_Item(344,482,402,540,mP):
      num = 26
    elif Get_Inv_Item(206,344,540,678,mP):
      num = 27
    elif Get_Inv_Item(344,482,540,678,mP):
      num = 28
    return num

def Get_9_Storage(mP):
    num = None
    if Get_Inv_Item(137,275,333,471,mP):
      num = 25
    elif Get_Inv_Item(275,413,333,471,mP):
      num = 26
    elif Get_Inv_Item(413,551,333,471,mP):
      num = 27 
    elif Get_Inv_Item(137,275,471,609,mP):
      num = 28
    elif Get_Inv_Item(275,413,471,609,mP):
      num = 29 
    elif Get_Inv_Item(413,551,471,609,mP):
      num = 30
    elif Get_Inv_Item(137,275,609,747,mP):
      num = 31
    elif Get_Inv_Item(275,413,609,747,mP):
      num = 32
    elif Get_Inv_Item(413,551,609,747,mP):
      num = 33
    return num

def Get_16_Storage(mP):
    num = None
    if Get_Inv_Item(68,206,264,392,mP):
      num = 25
    elif Get_Inv_Item(206,344,264,392,mP):
      num = 26
    elif Get_Inv_Item(344,482,264,392,mP):
      num = 27 
    elif Get_Inv_Item(482,620,264,392,mP):
      num = 28
    elif Get_Inv_Item(68,206,402,540,mP):
      num = 29 
    elif Get_Inv_Item(206,344,402,540,mP):
      num = 30
    elif Get_Inv_Item(344,482,402,540,mP):
      num = 31
    elif Get_Inv_Item(482,620,402,540,mP):
      num = 32
    elif Get_Inv_Item(68,206,540,678,mP):
      num = 33
    elif Get_Inv_Item(206,344,540,678,mP):
      num = 34
    elif Get_Inv_Item(344,482,540,678,mP):
      num = 35
    elif Get_Inv_Item(482,620,540,678,mP):
      num = 36
    elif Get_Inv_Item(68,206,678,816,mP):
      num = 37
    elif Get_Inv_Item(206,344,678,816,mP):
      num = 38
    elif Get_Inv_Item(344,482,678,816,mP):
      num = 39
    elif Get_Inv_Item(482,620,678,816,mP):
      num = 40
    return num

def Get_All_Inv_Items(mP,map):
    num = None
    if Get_Inv_Item(684,822,264,402,mP):
      num = 0 
    elif Get_Inv_Item(822,960,264,402,mP):
      num = 1
    elif Get_Inv_Item(960,1098,264,402,mP):
      num = 2 
    elif Get_Inv_Item(1098,1236,264,402,mP):
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
    elif Get_Inv_Item(753,891,100,238,mP):
      num = 16
    elif Get_Inv_Item(1029,1167,100,238,mP):
      num = 17
    elif Get_Inv_Item(509,647,850,988,mP):
      num = 18
    elif Get_Inv_Item(700,838,850,988,mP):
      num = 19
    elif Get_Inv_Item(891,1029,850,988,mP):
      num = 20
    elif Get_Inv_Item(1082,1220,850,988,mP):
      num = 21
    elif Get_Inv_Item(1273,1411,850,988,mP):
      num = 22
    elif Get_Inv_Item(1507,1645,100,238,mP):
      num = 23
    elif Get_Inv_Item(1507,1645,850,988,mP):
      num = 24
    if not player["objectOpen"][0] == None:
      object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
      if object["name"] == "Fired_Clay_Pot" and isinstance(Get_4_Storage(mP),int):
        num = Get_4_Storage(mP)
        return num
      elif (object["name"] == "Wood_Chest" or object["name"] == "Reinforced_Wood_Chest") and isinstance(Get_9_Storage(mP),int):
        num = Get_9_Storage(mP)
        return num
      elif (object["name"] == "Iron_Safe" or object["name"] == "Steel_Safe") and isinstance(Get_16_Storage(mP),int):
        num = Get_16_Storage(mP)
        return num
      else:
        return num
    else:
      return num


#######################################################################################################################################################################################

def Destroy_Item(sec,itemMap):
    for chunk in range(len(itemMap)):
      for item in range(len(itemMap[chunk]["chunk"])):
        if itemMap[chunk]["chunk"][item]["timeLeft"] == sec:
           itemMap[chunk]["chunk"].pop(item)

def Drop_Item(pos,itemMap,item,sec,size):
    if not item["baseInfo"]["type"] == None: 
      posX = pos[0]+(size[0]/2)-16
      posY = pos[1]+(size[1]/2)-16
      itemMap[Get_Chunk(int(posX/64),int(posY/64),mapChunkSize[0],32)]["chunk"].append({"position":[posX,posY],"timeLeft":sec+300,"item":item})

####################################################################################################################################################################################

def Item_Pick_Up_Non_Stacked(chunk,item):
  if Dist(chunk["chunk"][item]["position"][0],chunk["chunk"][item]["position"][1],player["position"][0]*64,player["position"][1]*64) < 75:
    for run in range(16):
      if player["inventory"][run] == items["none"]:
        player["inventory"][run] = chunk["chunk"][item]["item"]
        chunk["chunk"].pop(item)
        return -1
    return 0
  return 0

def Item_Pick_Up_Stacked(chunk,item):
  global player
  if Dist(chunk["chunk"][item]["position"][0],chunk["chunk"][item]["position"][1],player["position"][0]*64,player["position"][1]*64) < 75:
    for run in range(16):
      if player["inventory"][run]["baseInfo"] == chunk["chunk"][item]["item"]["baseInfo"]:
        if chunk["chunk"][item]["item"]["stack"][0] + player["inventory"][run]["stack"][0] <= player["inventory"][run]["stack"][1]:
          object = player["inventory"][run]["stack"][0] + chunk["chunk"][item]["item"]["stack"][0]
          player["inventory"][run]["stack"][0] = object
          chunk["chunk"].pop(item)
          return -1
        else:
          change = player["inventory"][run]["stack"][1] - player["inventory"][run]["stack"][0]
          player["inventory"][run]["stack"][0] = player["inventory"][run]["stack"][1]
          chunk["chunk"][item]["item"]["stack"][0] -= change
    for run in range(16):
      if player["inventory"][run] == items["none"]:
        player["inventory"][run] = chunk["chunk"][item]["item"]
        chunk["chunk"].pop(item)
        return -1
    return 0
  return 0

def Pick_up_item(chunk):
  minus = 0
  if len(chunk["chunk"]) > 0:
      for item in range(len(chunk["chunk"])):
        if chunk["chunk"][item+minus]["position"][0]-relativePerspective[0] >= -32 and chunk["chunk"][item+minus]["position"][0]-relativePerspective[0] <= WIDTH and chunk["chunk"][item+minus]["position"][1]-relativePerspective[1] >= -32 and chunk["chunk"][item+minus]["position"][1]-relativePerspective[1] <= HEIGHT:
          if chunk["chunk"][item+minus]["item"]["baseInfo"]["stacks"] == False:
            minus += Item_Pick_Up_Non_Stacked(chunk,item+minus)
          elif chunk["chunk"][item+minus]["item"]["baseInfo"]["stacks"] == True:
            minus += Item_Pick_Up_Stacked(chunk,item+minus)

########################################################################################################################################################################################

def Put_Back(sec,itemMap):
    if player["heldInvObject"]["index"] < 16 and player["inventory"][player["heldInvObject"]["index"]]["baseInfo"]["type"] == None:
      player["inventory"][player["heldInvObject"]["index"]] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 16 and player["leftHand"] == None:
      player["leftHand"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 17 and player["rightHand"] == None:
      player["rightHand"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 18 and player["helm"] == None:
      player["helm"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 19 and player["chest"] == None:
      player["chest"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 20 and player["legs"] == None:
      player["legs"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 21 and player["boots"] == None:
      player["boots"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 22 and player["gloves"] == None:
      player["gloves"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 23 and player["craftingTool"] == None:
      player["craftingTool"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    elif player["heldInvObject"]["index"] == 24 and player["craftingOutput"] == None:
      player["craftingOutput"] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
    else:
      Drop_Item((player["position"][0]*64+randint(-16,16),player["position"][1]*64+randint(-16,16)),itemMap,player["heldInvObject"]["item"],sec,[64,64])
      player["heldInvObject"]["item"] = items["none"]

def Put_Back_Stack(location,itemMap,sec,map):
    if location == "inventory":
      if player[location][player["heldInvObject"]["index"]]["baseInfo"]["type"] == None:
        player[location][player["heldInvObject"]["index"]] = player["heldInvObject"]["item"]
        player["heldInvObject"]["item"] = items["none"]  
      else:  
        player[location][player["heldInvObject"]["index"]]["stack"][0] += player["heldInvObject"]["item"]["stack"][0]
        player["heldInvObject"]["item"] = items["none"]  
    elif location == "rightHand" or location == "leftHand":
      if player[location]["baseInfo"]["type"] == None:
        player[location] = player["heldInvObject"]["item"]
        player["heldInvObject"]["item"] = items["none"]  
      else: 
        player[location]["stack"][0] += player["heldInvObject"]["item"]["stack"][0]
        player["heldInvObject"]["item"] = items["none"]
    elif location == "inv":
      object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
      if object[location][player["heldInvObject"]["index"]-25]["baseInfo"]["type"] == None:
        object[location][player["heldInvObject"]["index"]-25] = player["heldInvObject"]["item"]
        player["heldInvObject"]["item"] = items["none"]  
      else:  
        object[location][player["heldInvObject"]["index"]-25]["stack"][0] += player["heldInvObject"]["item"]["stack"][0]
        player["heldInvObject"]["item"] = items["none"]  
    else:
      Drop_Item((player["position"][0]*64+randint(-16,16),player["position"][1]*64+randint(-16,16)),itemMap,player["heldInvObject"]["item"],sec,[64,64])
      player["heldInvObject"]["item"] = items["none"]

def Place(num,location,map):
  if num < 16:
    player[location][num] = player["heldInvObject"]["item"]
    player["heldInvObject"]["item"] = items["none"]
  if num > 24:
    object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
    if object["type"] == "storage":
      object[location][num-25] = player["heldInvObject"]["item"]
      player["heldInvObject"]["item"] = items["none"]
  else:
    player[location] = player["heldInvObject"]["item"]
    player["heldInvObject"]["item"] = items["none"]

def Switch(num,location1,location2,map):
  if location2 == "inventory" and player["heldInvObject"]["index"] < 16:
    player[location1][player["heldInvObject"]["index"]] = player[location2][num]
    player[location2][num] = player["heldInvObject"]["item"]
    player["heldInvObject"]["item"] = items["none"]
  elif location2 == "inventory":
    player[location1] = player[location2][num]
    player[location2][num] = player["heldInvObject"]["item"]
    player["heldInvObject"]["item"] = items["none"]
  elif player["heldInvObject"]["index"] < 16:
    player[location1][player["heldInvObject"]["index"]] = player[location2]
    player[location2] = player["heldInvObject"]["item"]
    player["heldInvObject"]["item"] = items["none"]
  else:
    player[location1] = player[location2]
    player[location2] = player["heldInvObject"]["item"]
    player["heldInvObject"]["item"] = items["none"]

def Add_To_Stack(num,location,itemMap,sec,map):
  if num < 16:
    if player[location][num]["stack"][0] + player["heldInvObject"]["item"]["stack"][0] <= player[location][num]["stack"][1]:
      player[location][num]["stack"][0] += player["heldInvObject"]["item"]["stack"][0]
      player["heldInvObject"]["item"] = items["none"]
    else:
      change = player[location][num]["stack"][1] - player[location][num]["stack"][0]
      player[location][num]["stack"][0] = player[location][num]["stack"][1]
      player["heldInvObject"]["item"]["stack"][0] -= change
      Put_Back_Stack(location,itemMap,sec,map)
  elif num > 24:
    if location == "inv":
      object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
      if object[location][num-25]["stack"][0] + player["heldInvObject"]["item"]["stack"][0] <= object[location][num-25]["stack"][1]:
        object[location][num-25]["stack"][0] += player["heldInvObject"]["item"]["stack"][0]
        player["heldInvObject"]["item"] = items["none"]
      else:
        change = object[location][num-25]["stack"][1] - object[location][num-25]["stack"][0]
        object[location][num-25]["stack"][0] = object[location][num-25]["stack"][1]
        player["heldInvObject"]["item"]["stack"][0] -= change
        Put_Back_Stack(location,itemMap,sec,map)
  else:
    if player[location]["stack"][0] + player["heldInvObject"]["item"]["stack"][0] <= player[location]["stack"][1]:
      player[location]["stack"][0] += player["heldInvObject"]["item"]["stack"][0]
      player["heldInvObject"]["item"] = items["none"]
    else:
      change = player[location]["stack"][1] - player[location]["stack"][0]
      player[location]["stack"][0] = player[location]["stack"][1]
      player["heldInvObject"]["item"]["stack"][0] -= change
      Put_Back_Stack(location,itemMap,sec,map)

def Equipment_Switch(num,location,sec,itemMap):
  if player["heldInvObject"]["item"]["baseInfo"]["type"] == location:
    Switch(num,"inventory",location)
  else: 
    Put_Back(sec,itemMap)

def Equipment_Switch2(num,location,sec,itemMap):
  if (player["inventory"][num]["baseInfo"]["type"] == location or player["inventory"][num]["baseInfo"]["type"] == None) and (player["heldInvObject"]["item"]["baseInfo"]["type"] == location):
      Switch(num,location,"inventory")
  else: 
    Put_Back(sec,itemMap)

##############################################################################################################################################################################################

def Pick_Up(location,num):
      player["heldInvObject"]["item"] = player[location] 
      player[location] = items["none"]
      player["heldInvObject"]["index"] = num

def Object_Pick_Up(num,map):
      object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
      if object["type"] == "storage":
        player["heldInvObject"]["item"] = object["inv"][num-25] 
        object["inv"][num-25]  = items["none"]
        player["heldInvObject"]["index"] = num
        
  
def Half_Stack(num,location):
  stackSize = location["stack"][0]
  if stackSize % 2 == 0:
    player["heldInvObject"]["item"] = Convert_Item(location)
    player["heldInvObject"]["item"]["stack"][0] = stackSize//2
    location["stack"][0] = stackSize//2
    player["heldInvObject"]["index"] = num
  elif stackSize % 2 == 1:
    player["heldInvObject"]["item"] = Convert_Item(location)
    player["heldInvObject"]["item"]["stack"][0] = stackSize//2
    location["stack"][0] = stackSize//2 + 1
    player["heldInvObject"]["index"] = num

def Half_Stack_Object(num,map):
    object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
    if object["type"] == "storage":
      if object["inv"][num-25]["baseInfo"]["stacks"]:
        if not object["inv"][num-25]["stack"][0] == 1:
          stackSize = object["inv"][num-25]["stack"][0]
          if stackSize % 2 == 0:
            player["heldInvObject"]["item"] = Convert_Item(object["inv"][num-25])
            player["heldInvObject"]["item"]["stack"][0] = stackSize//2
            object["inv"][num-25]["stack"][0] = stackSize//2
            player["heldInvObject"]["index"] = num
          elif stackSize % 2 == 1:
            player["heldInvObject"]["item"] = Convert_Item(object["inv"][num-25])
            player["heldInvObject"]["item"]["stack"][0] = stackSize//2
            object["inv"][num-25]["stack"][0] = stackSize//2 + 1
            player["heldInvObject"]["index"] = num


def Remove_One(num,location):
  player["heldInvObject"]["item"] = Convert_Item(location)
  player["heldInvObject"]["item"]["stack"][0] = 1
  location["stack"][0] -= 1
  player["heldInvObject"]["index"] = num

def Remove_One_Object(num,map):
  object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
  if object["type"] == "storage":
    if object["inv"][num-25]["baseInfo"]["stacks"]:
      if not object["inv"][num-25]["stack"][0] == 1:
        player["heldInvObject"]["item"] = Convert_Item(object["inv"][num-25])
        player["heldInvObject"]["item"]["stack"][0] = 1
        object["inv"][num-25]["stack"][0] -= 1
        player["heldInvObject"]["index"] = num

#########################################################################################################################################################################################

def Tab_Switch(num,type,mP,itemMap,sec,shift,map):
  if type == 0:
    if leftRightMouseButton[0]:  
      if isinstance(num,int):
          if num < 16:
            player["heldInvObject"]["item"] = player["inventory"][num] 
            player["inventory"][num] = items["none"]
            player["heldInvObject"]["index"] = num
          elif num == 16:
            Pick_Up("leftHand",num)
          elif num == 17:
            Pick_Up("rightHand",num)
          elif num == 18:
            Pick_Up("helm",num)
          elif num == 19:
            Pick_Up("chest",num)
          elif num == 20:
            Pick_Up("legs",num)
          elif num == 21:
            Pick_Up("boots",num)
          elif num == 22:
            Pick_Up("gloves",num)
          elif num == 23:
            Pick_Up("craftingTool",num)
          elif num == 24:
            Pick_Up("craftingOutput",num)
          if not player["objectOpen"][0] == None and num > 24:
            Object_Pick_Up(num,map)

# # # # # #

    elif leftRightMouseButton[2] and not shift: 
      if isinstance(num,int):
          if num < 16 and player["inventory"][num]["baseInfo"]["stacks"]:
            if not player["inventory"][num]["stack"][0] == 1:
              Half_Stack(num,player["inventory"][num])
          elif num == 16 and player["leftHand"]["baseInfo"]["stacks"]:
            if not player["leftHand"]["stack"][0] == 1:
              Half_Stack(num,player["leftHand"])
          elif num == 17 and player["rightHand"]["baseInfo"]["stacks"]:
            if not player["rightHand"]["stack"][0] == 1:
              Half_Stack(num,player["rightHand"])
          if not player["objectOpen"][0] == None and num > 24:
            Half_Stack_Object(num,map)

# # # # # #

    elif leftRightMouseButton[2] and shift: 
      if isinstance(num,int):
        if num < 16 and player["inventory"][num]["baseInfo"]["stacks"]:
          if not player["inventory"][num]["stack"][0] == 1:
            Remove_One(num,player["inventory"][num])
        elif num == 16 and player["leftHand"]["baseInfo"]["stacks"]:
          if not player["leftHand"][num]["stack"][0] == 1:
            Remove_One(num,player["leftHand"])
        elif num == 17 and player["rightHand"]["baseInfo"]["stacks"]:
          if not player["rightHand"][num]["stack"][0] == 1:
            Remove_One(num,player["rightHand"])
        if not player["objectOpen"][0] == None and num > 24:
            Remove_One_Object(num,map)

# # # # # #

  if type == 1:
    if leftRightMouseButton[0]: 
      if isinstance(num,int):
                if num < 16:
                  if player["heldInvObject"]["index"] < 16:
                    if not player["heldInvObject"]["item"]["baseInfo"]["type"] == None:
                      if player["heldInvObject"]["item"]["baseInfo"]["name"] == player["inventory"][num]["baseInfo"]["name"] and player["heldInvObject"]["item"]["baseInfo"]["stacks"]:
                        if player["inventory"][num]["stack"][0] < player["inventory"][num]["stack"][1]:
                          Add_To_Stack(num,"inventory",itemMap,sec,map)
                        else:
                          Put_Back_Stack("inventory",itemMap,sec,map)
                      else:
                        Switch(num,"inventory","inventory")
                    else:
                      Put_Back(sec,itemMap)
                  elif player["heldInvObject"]["index"] == 16 and (player["inventory"][num]["baseInfo"]["type"] == "hand" or player["inventory"][num]["baseInfo"]["type"] == None) and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None: 
                        Switch(num,"leftHand","inventory")
                  elif player["heldInvObject"]["index"] == 17 and (player["inventory"][num]["baseInfo"]["type"] == "hand" or player["inventory"][num]["baseInfo"]["type"] == None) and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None: 
                        Switch(num,"rightHand","inventory")
                  elif player["heldInvObject"]["index"] == 18: 
                    Equipment_Switch2(num,"helm",sec,itemMap)
                  elif player["heldInvObject"]["index"] == 19: 
                    Equipment_Switch2(num,"chest",sec,itemMap)
                  elif player["heldInvObject"]["index"] == 20: 
                    Equipment_Switch2(num,"legs",sec,itemMap)
                  elif player["heldInvObject"]["index"] == 21: 
                    Equipment_Switch2(num,"boots",sec,itemMap)
                  elif player["heldInvObject"]["index"] == 22: 
                    Equipment_Switch2(num,"gloves",sec,itemMap)
                  elif player["heldInvObject"]["index"] == 23 and player["inventory"][num]["baseInfo"]["type"] == None and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None: 
                        Switch(num,"craftingTool","inventory")
                  elif player["heldInvObject"]["index"] == 24 and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None and player["inventory"][num]["baseInfo"]["type"] == None: 
                        Switch(num,"craftingOutput","inventory")
                  else:
                    Put_Back(sec,itemMap)
                elif num == 16:
                  if player["heldInvObject"]["index"] < 16 and player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand":
                    Switch(num,"inventory","leftHand")
                  elif player["heldInvObject"]["index"] == 17 and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None:
                    Switch(num,"rightHand","leftHand")
                  elif player["heldInvObject"]["index"] == 23 and player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand":
                    if player["leftHand"]["baseInfo"]["type"] == None:
                      Switch(num,"craftingTool","leftHand")
                    elif player["leftHand"]["second"] == "knife" or player["leftHand"]["second"] == "hammer" or player["leftHand"]["second"] == "screwDriver":
                      Switch(num,"craftingTool","leftHand")
                    else:
                      Put_Back(sec,itemMap)
                  elif player["heldInvObject"]["index"] == 24 and player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand" and player["leftHand"]["baseInfo"]["type"] == None:
                    Place(num,"leftHand",map)
                  else: 
                    Put_Back(sec,itemMap)
                elif num == 17:
                  if player["heldInvObject"]["index"] < 16 and player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand":
                    Switch(num,"inventory","rightHand")
                  elif player["heldInvObject"]["index"] == 16 and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None:
                    Switch(num,"rightHand","rightHand")
                  elif player["heldInvObject"]["index"] == 23 and player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand":
                    if player["rightHand"]["baseInfo"]["type"] == None:
                      Switch(num,"craftingTool","rightHand")
                    elif player["rightHand"]["second"] == "knife" or player["rightHand"]["second"] == "hammer" or player["rightHand"]["second"] == "screwDriver":
                      Switch(num,"craftingTool","rightHand")
                  elif player["heldInvObject"]["index"] == 24 and player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand" and player["rightHand"]["baseInfo"]["type"] == None:
                    Place(num,"rightHand",map)
                  else: 
                    Put_Back(sec,itemMap)
                elif num == 18:
                  Equipment_Switch(num,"helm",sec,itemMap)
                elif num == 19:
                  Equipment_Switch(num,"chest",sec,itemMap)
                elif num == 20:
                  Equipment_Switch(num,"legs",sec,itemMap)
                elif num == 21:
                  Equipment_Switch(num,"boots",sec,itemMap)
                elif num == 22:
                  Equipment_Switch(num,"gloves",sec,itemMap)
                elif num == 23 and player["craftingTool"]["baseInfo"]["type"] == None and player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand": 
                  if player["heldInvObject"]["item"]["first"] == "tool" and (player["heldInvObject"]["item"]["second"] == "knife" or player["heldInvObject"]["item"]["second"] == "hammer" or player["heldInvObject"]["item"]["second"] == "screwDriver"):
                    Place(num,"craftingTool",map)
                  else: 
                    Put_Back(sec,itemMap)
                elif num == 24: 
                      Put_Back(sec,itemMap)
                elif num > 24:
                  object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
                  if object["type"] == "storage":
                    if player["heldInvObject"]["index"] < 16:
                      if not player["heldInvObject"]["item"]["baseInfo"]["type"] == None:
                        if player["heldInvObject"]["item"]["baseInfo"]["name"] == player["inventory"][num]["baseInfo"]["name"] and player["heldInvObject"]["item"]["baseInfo"]["stacks"]:
                          if object["inv"][num]["stack"][0] < object["inv"][num]["stack"][1]:
                            Add_To_Stack(num,"inv",itemMap,sec,map) 
                          else:
                            Put_Back_Stack("inv",itemMap,sec,map)
                        else:
                          Switch(num,"inv","inventory") #
                      else:
                        Put_Back(sec,itemMap)
                    elif player["heldInvObject"]["index"] == 16 and (player["inventory"][num]["baseInfo"]["type"] == "hand" or player["inventory"][num]["baseInfo"]["type"] == None) and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None: 
                          Switch(num,"leftHand","inventory")
                    elif player["heldInvObject"]["index"] == 17 and (player["inventory"][num]["baseInfo"]["type"] == "hand" or player["inventory"][num]["baseInfo"]["type"] == None) and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None: 
                          Switch(num,"rightHand","inventory")
                    elif player["heldInvObject"]["index"] == 18: 
                      Equipment_Switch2(num,"helm",sec,itemMap)
                    elif player["heldInvObject"]["index"] == 19: 
                      Equipment_Switch2(num,"chest",sec,itemMap)
                    elif player["heldInvObject"]["index"] == 20: 
                      Equipment_Switch2(num,"legs",sec,itemMap)
                    elif player["heldInvObject"]["index"] == 21: 
                      Equipment_Switch2(num,"boots",sec,itemMap)
                    elif player["heldInvObject"]["index"] == 22: 
                      Equipment_Switch2(num,"gloves",sec,itemMap)
                    elif player["heldInvObject"]["index"] == 23 and player["inventory"][num]["baseInfo"]["type"] == None and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None: 
                          Switch(num,"craftingTool","inventory")
                    elif player["heldInvObject"]["index"] == 24 and not player["heldInvObject"]["item"]["baseInfo"]["type"] == None and player["inventory"][num]["baseInfo"]["type"] == None: 
                          Switch(num,"craftingOutput","inventory")
                    else:
                      Put_Back(sec,itemMap)
                else:
                  Put_Back(sec,itemMap)
      else: 
        if not player["heldInvObject"]["item"]["baseInfo"]["type"] == None:
          itemMap = Drop_Item((mP[0]+relativePerspective[0]-16,mP[1]+relativePerspective[1]-16),itemMap,player["heldInvObject"]["item"],sec,[32,32])
          player["heldInvObject"]["item"] = items["none"]

# # # # # #

    elif leftRightMouseButton[2]:
      if isinstance(num,int):
        if num < 16:
          if player["inventory"][num]["baseInfo"]["type"] == None:
            Place(num,"inventory",map)
          elif player["inventory"][num]["baseInfo"]["name"] == player["heldInvObject"]["item"]["baseInfo"]["name"]:
            if player["inventory"][num]["stack"][0] < player["inventory"][num]["stack"][1]:
              Add_To_Stack(num,"inventory",itemMap,sec,map)
            else:
              Put_Back_Stack("inventory",itemMap,sec,map)
          else:
            Put_Back_Stack("inventory",itemMap,sec,map)
        elif num == 16:
          if player["leftHand"]["baseInfo"]["type"] == None:
            if player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand":
              Place(num,"leftHand",map)
            else:
              Put_Back_Stack("leftHand",itemMap,sec,map)
          elif player["leftHand"]["baseInfo"]["name"] == player["heldInvObject"]["item"]["baseInfo"]["name"]:
            if player["leftHand"]["stack"][0] < player["leftHand"]["stack"][1]:
              Add_To_Stack(num,"leftHand",itemMap,sec,map)
            else:
              Put_Back_Stack("leftHand",itemMap,sec,map)
        elif num == 17:
          if player["rightHand"]["baseInfo"]["type"] == None:
            if player["heldInvObject"]["item"]["baseInfo"]["type"] == "hand":
              Place(num,"rightHand",map)
            else:
              Put_Back_Stack("rightHand",itemMap,sec,map)
          elif player["rightHand"]["baseInfo"]["name"] == player["heldInvObject"]["item"]["baseInfo"]["name"]:
            if player["rightHand"]["stack"][0] < player["rightHand"]["stack"][1]:
              Add_To_Stack(num,"rightHand",map)
            else:
              Put_Back_Stack("rightHand",itemMap,sec,map)
        elif num > 24:
            object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
            if object["type"] == "storage":
              if object["inv"][num-25]["baseInfo"]["type"] == None:
                Place(num,"inv",map)
              elif object["inv"][num-25]["baseInfo"]["name"] == player["heldInvObject"]["item"]["baseInfo"]["name"]:
                if object["inv"][num-25]["stack"][0] < object["inv"][num-25]["stack"][1]:
                  Add_To_Stack(num,"inv",itemMap,sec,map)
                else:
                  Put_Back_Stack("inv",itemMap,sec,map)
              else:
                Put_Back_Stack("inv",itemMap,sec,map)
      else: 
        if not player["heldInvObject"]["item"]["baseInfo"]["type"] == None:
          itemMap = Drop_Item((mP[0]+relativePerspective[0]-16,mP[1]+relativePerspective[1]-16),itemMap,player["heldInvObject"]["item"],sec,[32,32])
          player["heldInvObject"]["item"] = items["none"]

def Can_Hold_None_Stacked(location,sec,itemMap):
    for run in range(16):
      if player["inventory"][run] == items["none"]:
        player["inventory"][run] = player[location]
        player[location] = items["none"]
        break
    Drop_Item((player["position"][0]*64+randint(-16,16),player["position"][1]*64+randint(-16,16)),itemMap,player[location],sec,[64,64])
    player[location] = items["none"]

def Can_Hold_Stacked(location,sec,itemMap):
    for run in range(16):
      if player["inventory"][run]["baseInfo"] == player[location]["baseInfo"]:
        if player[location]["stack"][0] + player["inventory"][run]["stack"][0] <= player["inventory"][run]["stack"][1]:
          object = player["inventory"][run]["stack"][0] + player[location]["stack"][0]
          player["inventory"][run]["stack"][0] = object
          player[location] = items["none"]
          break
        else:
          change = player["inventory"][run]["stack"][1] - player["inventory"][run]["stack"][0]
          player["inventory"][run]["stack"][0] = player["inventory"][run]["stack"][1]
          player[location]["stack"][0] -= change
    for run in range(16):
      if player["inventory"][run] == items["none"]:
        player["inventory"][run] = player[location]
        player[location] = items["none"]
        break
    Drop_Item((player["position"][0]*64+randint(-16,16),player["position"][1]*64+randint(-16,16)),itemMap,player[location],sec,[64,64])
    player[location] = items["none"]

def Close_Inv(sec,itemMap):
    if not player["heldInvObject"]["item"]["baseInfo"]["type"] == None:
      if not player["heldInvObject"]["item"]["baseInfo"]["stacks"]:
        Put_Back(sec,itemMap)
      else:
        if player["heldInvObject"]["index"] < 16:
          Put_Back_Stack("inventory",itemMap,sec)
        elif player["heldInvObject"]["index"] == 16:
          Put_Back_Stack("leftHand",itemMap,sec)
        elif player["heldInvObject"]["index"] == 17:
          Put_Back_Stack("rightHand",itemMap,sec)
    if not player["craftingTool"]["baseInfo"]["type"] == None:
      if not player["craftingTool"]["baseInfo"]["stacks"]:
        Can_Hold_None_Stacked("craftingTool",sec,itemMap)
      else:
        Can_Hold_Stacked("craftingTool",sec,itemMap)
    if not player["craftingOutput"]["baseInfo"]["type"] == None:
      if not player["craftingOutput"]["baseInfo"]["stacks"]:
        Can_Hold_None_Stacked("craftingOutput",sec,itemMap)
      else:
        Can_Hold_Stacked("craftingOutput",sec,itemMap)
      

####################################################################################################################################################################################
        
def Check_If_Block_Pix(map,activeMap,mP):
    if map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["type"] == None:
      for x in range(len(activeMap[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"])):
          if activeMap[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][x]["blockPosition"][0] == Get_Square_Cord(mP[0],mP[1])[0] and activeMap[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][x]["blockPosition"][1] == Get_Square_Cord(mP[0],mP[1])[1]:
            return True
      return False
    else:
      return True
    
def Check_If_Block_Cord(map,activeMap,cords):
    if map[Get_Chunk(cords[0],cords[1],mapChunkSize[0],32)]["chunk"][Get_Square(cords[0],cords[1],32)]["baseBlock"]["type"] == None:
      for x in range(len(activeMap[Get_Chunk(cords[0],cords[1],mapChunkSize[0],32)]["chunk"])):
          if activeMap[Get_Chunk(cords[0],cords[1],mapChunkSize[0],32)]["chunk"][x]["blockPosition"][0] == cords[0] and activeMap[Get_Chunk(cords[0],cords[1],mapChunkSize[0],32)]["chunk"][x]["blockPosition"][1] == cords[1]:
            return True
      return False
    else:
      return True

####################################################################################################################################################################################

def Destroy_Block(mP,hand,map,itemMap,sec,blockType):
   object = map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]
   if not object["baseBlock"]["type"] == None:
    if object["baseBlock"]["type"] == blockType and player[hand]["tier"] >= object["baseBlock"]["tier"] and Dist(object["position"][0],object["position"][1],player["position"][0],player["position"][1]) <= 4:
      player[hand]["durability"][0] -= 1
      map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"][0] -= player[hand]["damage"]*object["baseBlock"]["resistance"]
      if player[hand]["durability"][0] <= 0:
        player[hand] = items["none"]
      if map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"][0] <= 0:
        for item in range(object["baseBlock"]["dropTable"][1]):
          Drop_Item((object["position"][0]*64+randint(-16,16),object["position"][1]*64+randint(-16,16)),itemMap,Pick_Loot(object["baseBlock"]["dropTable"][0]),sec,[64,64]) 
        map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"] = baseBlocks["none"]
    elif object["baseBlock"]["tier"] <= 0  and Dist(object["position"][0],object["position"][1],player["position"][0],player["position"][1]) <= 4:
      map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"][0] -= 1*object["baseBlock"]["resistance"]
      if map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"][0] <= 0:
        for item in range(object["baseBlock"]["dropTable"][1]):
          Drop_Item((object["position"][0]*64+randint(-16,16),object["position"][1]*64+randint(-16,16)),itemMap,Pick_Loot(object["baseBlock"]["dropTable"][0]),sec,[64,64]) 
        map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"] = baseBlocks["none"]

##################################################################################################################################################################################3

def Place_Block(mP,hand,map,activeMap):
  blockPos = Get_Square_Cord(mP[0],mP[1])
  if Dist(player["position"][0],player["position"][1],blockPos[0],blockPos[1]) <=4:
      if not Check_If_Block_Pix(map,activeMap,mP):
        if player[hand]["second"] == "active":
          item = Convert_Blocks(activeBlocks[player[hand]["baseInfo"]["name"]])
          item["blockPosition"][0] = blockPos[0]
          item["blockPosition"][1] = blockPos[1]
          activeMap[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"].append(item)
          player[hand] = items["none"]
        elif player[hand]["second"] == "inActive":
          item = Convert_Blocks(baseBlocks[player[hand]["baseInfo"]["name"]])
          map[Get_Chunk_Clicked(mapChunkSize[0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,mP[0],mP[1])]["baseBlock"] = item
          player[hand] = items["none"]

##################################################################################################################################################################################

def Use_Hand_Item(mP,hand,LRNum,map,itemMap,activeMap,sec):
  if (LRNum[0] and hand == "leftHand") or (LRNum[2] and hand == "rightHand"):
    if player[hand]["baseInfo"]["type"] == "hand":
      if player[hand]["first"] == "tool":
        if player[hand]["second"] == "pick":
          Destroy_Block(mP,hand,map,itemMap,sec,"rock")
        elif player[hand]["second"] == "axe":
          Destroy_Block(mP,hand,map,itemMap,sec,"wood")
      elif player[hand]["first"] == "block":
        Place_Block(mP,hand,map,activeMap)
    elif player[hand]["baseInfo"]["type"] == None:
      Destroy_Block(mP,hand,map,itemMap,sec,"")

def Use_Pressed_Down(mP,tick,map,activeMap,itemMap,sec,hand):
        if not player[hand]["speed"] == 0:
          if not invOn:
            if tick % player[hand]["speed"] == 0:
              Use_Hand_Item(mP,hand,leftRightMouseButton,map,itemMap,activeMap,sec)

def Use_Clicked(map,activeMap,itemMap,sec,hand):
  if not player[hand]["baseInfo"]["type"] == None:
    if player[hand]["speed"] == 0 and player[hand]["coolDown"] == 0:
      mP = pygame.mouse.get_pos()
      leftRightMouseButton = pygame.mouse.get_pressed()
      if not invOn:
          Use_Hand_Item(mP,hand,leftRightMouseButton,map,itemMap,activeMap,sec)

###################################################################################################################################################################################

def Move_Line(map,activeMap,speed,xy,x,y):
  if not Check_If_Block_Cord(map,activeMap,[player["position"][0]+x,player["position"][1]+y]):
    player["position"][xy] += y+x
    player["stam"][0] -= speed

def Move_Diagonal(map,activeMap,speed,x,y):
  if not Check_If_Block_Cord(map,activeMap,[player["position"][0]+x,player["position"][1]+y]) and If_Both_False(Check_If_Block_Cord(map,activeMap,[player["position"][0],player["position"][1]+y]),Check_If_Block_Cord(map,activeMap,[player["position"][0]+x,player["position"][1]])):
        player["position"][0] += x
        player["position"][1] += y
        player["stam"][0] -= speed

def Move_Player(map,activeMap,speed):
    if w and a and player["position"][1] > 0 and player["position"][0] > 0 and player["stam"][0] > speed:
      Move_Diagonal(map,activeMap,speed,-1,-1)
    elif w and d and player["position"][1] > 0 and player["position"][0] < mapChunkSize[0]*32-1 and player["stam"][0] > speed:
      Move_Diagonal(map,activeMap,speed,1,-1)
    elif s and a and player["position"][1] < mapChunkSize[1]*32-1 and player["position"][0] > 0 and player["stam"][0] > speed:
      Move_Diagonal(map,activeMap,speed,-1,1)
    elif s and d and player["position"][0] < mapChunkSize[0]*32-1 and player["position"][1] < mapChunkSize[0]*32-1  and player["stam"][0] > speed: 
      Move_Diagonal(map,activeMap,speed,1,1)
    elif w and player["position"][1] > 0 and player["stam"][0] > speed:
      Move_Line(map,activeMap,speed,1,0,-1)
    elif a and player["position"][0] > 0 and player["stam"][0] > speed:
      Move_Line(map,activeMap,speed,0,-1,0)
    elif s and player["position"][1] < mapChunkSize[1]*32-1 and player["stam"][0] > speed:
      Move_Line(map,activeMap,speed,1,0,1)
    elif d and player["position"][0] < mapChunkSize[0]*32-1 and player["stam"][0] > speed: 
      Move_Line(map,activeMap,speed,0,1,0)

#######################################################################################################################################################################################           
        
def Get_Keyboard_Events_Single_Player_Mode(map,itemMap,activeMap,sec,tick):
    global running
    global mousePosition
    global tempMousePosition
    global relativePerspective
    global mouseState
    global invOn
    global leftRightMouseButton
    global shift
    global w
    global a
    global s
    global d
    speed = 10
    tickSpeed = 10
    mP = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
          running = False

        if event.type == pygame.KEYDOWN:
          if event.key == pygame.K_LSHIFT:
            shift = True
          if event.key == pygame.K_w:
            w = True
          if event.key == pygame.K_a:
            a = True
          if event.key == pygame.K_s:
            s = True
          if event.key == pygame.K_d:
            d = True
          if event.key == pygame.K_TAB and invOn: ### TAB
             invOn = False
             player["objectOpen"] = [None,None]
             Close_Inv(sec,itemMap)
          elif event.key == pygame.K_TAB and not invOn:
             invOn = True

          if event.key == pygame.K_e and not invOn: ### TAB
            if Check_If_Block_Cord(map,activeMap,[player["position"][0]+viewCord[int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][0],player["position"][1]+viewCord[int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][1]]):
              if map[Get_Chunk(player["position"][0]+viewCord[int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][0],player["position"][1]+viewCord[int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["position"][0]+viewCord[int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][0],player["position"][1]+viewCord[int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][1],32)]["baseBlock"]["type"] == "storage":
                player["objectOpen"] = [player["position"][0]+viewCord[int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][0],player["position"][1]+viewCord[int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-337.5)//45)][1]]
                invOn = True
          elif event.key == pygame.K_e and invOn: 
              if not player["objectOpen"][0] == None:
                player["objectOpen"] = [None,None]
                invOn = False

          if event.key == pygame.K_1 and not invOn: 
             Hotbar_Quick_Change(0,"leftHand")
          if event.key == pygame.K_2 and not invOn:
             Hotbar_Quick_Change(1,"leftHand")
          if event.key == pygame.K_3 and not invOn:
             Hotbar_Quick_Change(2,"rightHand")
          if event.key == pygame.K_4 and not invOn:
             Hotbar_Quick_Change(3,"rightHand")

        if event.type == pygame.MOUSEBUTTONDOWN and mouseState == "up": ### TAB
          mouseState = 'down'
          leftRightMouseButton = pygame.mouse.get_pressed()

          if invOn:
            if player["craftingTool"]["baseInfo"]["type"] == None:
              Get_Assemble_Items(mP)
            elif player["craftingTool"]["second"] == "knife":
              Get_Carve_Items(mP) 
            num = Get_All_Inv_Items(mP,map)
            Tab_Switch(num,0,mP,itemMap,sec,shift,map)

          else:
            Use_Clicked(map,activeMap,itemMap,sec,"leftHand")
            Use_Clicked(map,activeMap,itemMap,sec,"rightHand")

        if event.type == pygame.MOUSEBUTTONUP and mouseState == "down":
            mouseState = 'up'
            if invOn and not player["heldInvObject"]["item"] == items["none"]:
              num = Get_All_Inv_Items(mP,map)
              Tab_Switch(num,1,mP,itemMap,sec,shift,map)
              
        if event.type == pygame.KEYUP:
          if event.key == pygame.K_LSHIFT:
            shift = False
          if event.key == pygame.K_w:
            w = False
          if event.key == pygame.K_a:
            a = False
          if event.key == pygame.K_s:
            s = False
          if event.key == pygame.K_d:
            d = False

    if shift:
      tickSpeed = 7

    if tick % tickSpeed == 0 and not invOn:
      Move_Player(map,activeMap,speed)

    if mouseState == "down":
      leftRightMouseButton = pygame.mouse.get_pressed()
      Use_Pressed_Down(mP,tick,map,activeMap,itemMap,sec,"leftHand")
      Use_Pressed_Down(mP,tick,map,activeMap,itemMap,sec,"rightHand")
              
    relativePerspective[0] = player["position"][0]*64-928
    relativePerspective[1] = player["position"][1]*64-508
  
########################################################################################################################################################################################

def Get_Sprite(sheet,colour,spriteSize):
    sprite = pygame.Surface((spriteSize,spriteSize))
    sprite.blit(sheet,(0,0),(0,0,spriteSize,spriteSize))
    sprite = pygame.transform.scale(sprite, (spriteSize, spriteSize))
    sprite.set_colorkey(colour)
    return sprite

# # # # # #

def Draw_Word(word,xy):
    total = 0
    for letter in word:
      Win.blit(Get_Sprite(LO(f"LN/{letter}"),(0,0,0),64),[xy[0]+total*6,xy[1]])
      total += 1

def Draw_Chunk(chunk):
    for block in range(1024):
       if chunk["chunk"][block]["position"][0]*64-relativePerspective[0] >= -64 and chunk["chunk"][block]["position"][0]*64-relativePerspective[0] <= WIDTH and chunk["chunk"][block]["position"][1]*64-relativePerspective[1] >= -64 and chunk["chunk"][block]["position"][1]*64-relativePerspective[1] <= HEIGHT:
          Win.blit(Get_Sprite(chunk["chunk"][block]["floorBlock"]["sprites"],(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-relativePerspective[0],chunk["chunk"][block]["position"][1]*64-relativePerspective[1])))
          if not chunk["chunk"][block]["baseBlock"]["sprites"] == None:
            Win.blit(Get_Sprite(chunk["chunk"][block]["baseBlock"]["sprites"],(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-relativePerspective[0],chunk["chunk"][block]["position"][1]*64-relativePerspective[1])))
            num = int(chunk["chunk"][block]["baseBlock"]["hp"][0]//(chunk["chunk"][block]["baseBlock"]["hp"][1]//5))
            if not num == 5:
              Win.blit(Get_Sprite(LO(f"blockBreaking/blockBreak{num}"),(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-relativePerspective[0],chunk["chunk"][block]["position"][1]*64-relativePerspective[1])))

def Draw_Screen(map):
    chunkSpot = player["position"][0]-(((player["position"][0])//32)*32),player["position"][1]-(((player["position"][1])//32)*32)
    inChunk = map[Get_Chunk(player["position"][0],player["position"][1],mapChunkSize[0],32)]["chunkPosition"]
    chunkCords = Get_Chunks_To_Draw(mapChunkSize[0],mapChunkSize[1],inChunk[0],inChunk[1],chunkSpot[0],chunkSpot[1])
    for chunk in range(len(chunkCords)):
      Draw_Chunk(map[Get_Chunk((((chunkCords[chunk][0]+1)*32)-1),(((chunkCords[chunk][1]+1)*32)-1),mapChunkSize[0],32)])

def Draw_Active_Chunk(chunk):
    if len(chunk["chunk"]) > 0:
      for item in range(len(chunk["chunk"])):
        if chunk["chunk"][item]["blockPosition"][0]*64-relativePerspective[0] >= -32 and chunk["chunk"][item]["blockPosition"][0]*64-relativePerspective[0] <= WIDTH and chunk["chunk"][item]["blockPosition"][1]*64-relativePerspective[1] >= -32 and chunk["chunk"][item]["blockPosition"][1]*64-relativePerspective[1] <= HEIGHT:
          if chunk["chunk"][item]["active"]:
            Win.blit(Get_Sprite(chunk["chunk"][item]["onSprite"],(0,0,0),64),((chunk["chunk"][item]["blockPosition"][0]*64-relativePerspective[0],chunk["chunk"][item]["blockPosition"][1]*64-relativePerspective[1])))
          else:
            Win.blit(Get_Sprite(chunk["chunk"][item]["offSprite"],(0,0,0),64),((chunk["chunk"][item]["blockPosition"][0]*64-relativePerspective[0],chunk["chunk"][item]["blockPosition"][1]*64-relativePerspective[1])))


def Draw_Active_Screen(map):
    chunkSpot = player["position"][0]-(((player["position"][0])//32)*32),player["position"][1]-(((player["position"][1])//32)*32)
    inChunk = map[Get_Chunk(player["position"][0],player["position"][1],mapChunkSize[0],32)]["chunkPosition"]
    chunkCords = Get_Chunks_To_Draw(mapChunkSize[0],mapChunkSize[1],inChunk[0],inChunk[1],chunkSpot[0],chunkSpot[1])
    for chunk in range(len(chunkCords)):
      Draw_Active_Chunk(map[Get_Chunk((((chunkCords[chunk][0]+1)*32)-1),(((chunkCords[chunk][1]+1)*32)-1),mapChunkSize[0],32)])


def Draw_Item_Chunk(chunk):
    global player
    global relativePerspective
    if len(chunk["chunk"]) > 0:
      for item in range(len(chunk["chunk"])):
        if chunk["chunk"][item]["position"][0]-relativePerspective[0] >= -32 and chunk["chunk"][item]["position"][0]-relativePerspective[0] <= WIDTH and chunk["chunk"][item]["position"][1]-relativePerspective[1] >= -32 and chunk["chunk"][item]["position"][1]-relativePerspective[1] <= HEIGHT:
          Win.blit(Get_Sprite(chunk["chunk"][item]["item"]["baseInfo"]["itemSprite"],(0,0,0),64),((chunk["chunk"][item]["position"][0]-relativePerspective[0],chunk["chunk"][item]["position"][1]-relativePerspective[1])))

def Draw_Screen_Items(map):
    chunkSpot = player["position"][0]-(((player["position"][0])//32)*32),player["position"][1]-(((player["position"][1])//32)*32)
    inChunk = map[Get_Chunk(player["position"][0],player["position"][1],mapChunkSize[0],32)]["chunkPosition"]
    chunkCords = Get_Chunks_To_Draw(mapChunkSize[0],mapChunkSize[1],inChunk[0],inChunk[1],chunkSpot[0],chunkSpot[1])
    for chunk in range(len(chunkCords)):
      Draw_Item_Chunk(map[Get_Chunk((((chunkCords[chunk][0]+1)*32)-1),(((chunkCords[chunk][1]+1)*32)-1),mapChunkSize[0],32)])
      Pick_up_item(map[Get_Chunk((((chunkCords[chunk][0]+1)*32)-1),(((chunkCords[chunk][1]+1)*32)-1),mapChunkSize[0],32)])

# # # # # #

def Get_Durability_Color(itemDurability):
    if itemDurability > 0.5:
        return(int(255-(255*((itemDurability-0.5)*2))),255,0)
    if itemDurability < 0.5:
        return(255,int(255*(itemDurability*2)),0)
    if itemDurability == 0.5:
        return(255,255,0)

def Draw_Inv_Item(location,x,y):
  Win.blit(Get_Sprite(LO("playerStuff/invItem"),(0,0,0),138),[x,y])
  if not player[location]["baseInfo"]["type"] == None:
    Win.blit(Get_Sprite(player[location]["baseInfo"]["invSprite"],(0,0,0),128),[x+5,y+5])
    if player[location]["baseInfo"]["type"] == "hand":
      if player[location]["first"] == "tool":
        pygame.draw.polygon(Win,Get_Durability_Color(player[location]["durability"][0]/player[location]["durability"][1]),[(x+5,y+132),(x+5+(128*(player[location]["durability"][0]/player[location]["durability"][1])),y+132),(x+5+(128*(player[location]["durability"][0]/player[location]["durability"][1])),y+131),(x+5,y+131)])

def Draw_Assembley():
    Win.blit(Get_Sprite(LO("playerStuff/invItem"),(0,0,0),138),[1305,269])
    Win.blit(Get_Sprite(LO("invView/stoneKnife"),(0,0,0),128),[1307,274])
    Win.blit(Get_Sprite(LO("playerStuff/invItem"),(0,0,0),138),[1444,269])
    Win.blit(Get_Sprite(LO("invView/stoneAxe"),(0,0,0),128),[1449,274])
    Win.blit(Get_Sprite(LO("playerStuff/invItem"),(0,0,0),138),[1583,269])
    Win.blit(Get_Sprite(LO("invView/campFire"),(0,0,0),128),[1588,274])

def Draw_A_Ingredients(name,mp):
    total = 0
    for set in assembely[name]["ingredients"]:
      Draw_Word(name,[mp[0],mp[1]-10])
      Draw_Word(set[0],[mp[0],mp[1]+20+(total*12)])
      Draw_Word(str(set[1]),[mp[0]-16,mp[1]+20+(total*12)])
      total += 1

def Draw_Assembley_Ingredients(mp):
    if Get_Inv_Item(1305,1443,269,407,mp):
      Draw_A_Ingredients("Stone_Knife",mp)
    if Get_Inv_Item(1444,1582,269,407,mp):
      Draw_A_Ingredients("Stone_Axe",mp)
    if Get_Inv_Item(1583,1721,269,407,mp):
      Draw_A_Ingredients("Camp_Fire",mp)

def Draw_C_Ingredients(name,mp):
    total = 0
    for set in carving[name]["ingredients"]:
      Draw_Word(name,[mp[0],mp[1]-10])
      Draw_Word(set[0],[mp[0],mp[1]+20+(total*12)])
      Draw_Word(str(set[1]),[mp[0]-16,mp[1]+20+(total*12)])
      total += 1

def Draw_Carve_Ingredients(mp):
    if Get_Inv_Item(1305,1443,269,407,mp):
      Draw_C_Ingredients("Pry_Stick",mp)
    if Get_Inv_Item(1444,1582,269,407,mp):
      Draw_C_Ingredients("Wood_Axe_Handle",mp)

def Draw_Carve():
    Win.blit(Get_Sprite(LO("playerStuff/invItem"),(0,0,0),138),[1305,269])
    Win.blit(Get_Sprite(LO("invView/pryStick"),(0,0,0),128),[1307,274])
    Win.blit(Get_Sprite(LO("playerStuff/invItem"),(0,0,0),138),[1444,269])
    Win.blit(Get_Sprite(LO("invView/woodAxeHandle"),(0,0,0),128),[1449,274])

def Draw_Grid_Objects(gridSize,xy,object):
    for item in range(gridSize[0]*gridSize[1]):
         if not object["inv"][item]["baseInfo"]["type"] == None: 
          Win.blit(Get_Sprite(object["inv"][item]["baseInfo"]["invSprite"],(0,0,0),128),[(item%gridSize[0]*138)+xy[0],(item//gridSize[0]*138)+xy[1]])
          if object["inv"][item]["baseInfo"]["stacks"]:
            num = object["inv"][item]["stack"][0]
            Win.blit(Get_Sprite(LO(f"LN/{num}"),(0,0,0),9),[(item%gridSize[0]*138)+xy[0],(item//gridSize[0]*138)+xy[1]])
          elif object["inv"][item]["baseInfo"]["type"] == "hand":
            if object["inv"][item]["first"] == "tool":
              pygame.draw.polygon(Win,Get_Durability_Color(object["inv"][item]["durability"][0]/object["inv"][item]["durability"][1]),[((item%gridSize[0]*138)+xy[0],(item//gridSize[0]*138)+xy[1]+128),((item%gridSize[0]*138)+xy[0]+(128*(object["inv"][item]["durability"][0]/object["inv"][item]["durability"][1])),(item//gridSize[0]*138)+xy[1]+128),((item%gridSize[0]*138)+xy[0]+(128*(object["inv"][item]["durability"][0]/object["inv"][item]["durability"][1])),(item//gridSize[0]*138)+xy[1]+127),((item%gridSize[0]*138)+xy[0],(item//gridSize[0]*138)+xy[1]+127)])

def Draw_Open_Object(map):
    object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
    if object["name"] == "Fired_Clay_Pot":
      Win.blit(Get_Sprite(LO("objectViews/4Storage"),(0,0,0),1920),[206,402])
      Draw_Grid_Objects([2,2],[211,407],object)
    if object["name"] == "Wood_Chest" or object["name"] == "Reinforced_Wood_Chest":
      Win.blit(Get_Sprite(LO("objectViews/9Storage"),(0,0,0),1920),[137,333])
      Draw_Grid_Objects([3,3],[142,338],object)
    if object["name"] == "Iron_Safe" or object["name"] == "Steel_Safe":
      Win.blit(Get_Sprite(LO("objectViews/16Storage"),(0,0,0),1920),[68,264])
      Draw_Grid_Objects([4,4],[73,269],object)

def Draw_Inv(mP):
    Win.blit(Get_Sprite(LO("playerStuff/inv"),(0,0,0),552),(684,264))
    for item in range(16):
        if not player["inventory"][item]["baseInfo"]["type"] == None: 
          Win.blit(Get_Sprite(player["inventory"][item]["baseInfo"]["invSprite"],(0,0,0),128),[(item%4*138)+689,(item//4*138)+269])
          if player["inventory"][item]["baseInfo"]["stacks"]:
            num = player["inventory"][item]["stack"][0]
            Win.blit(Get_Sprite(LO(f"LN/{num}"),(0,0,0),9),[(item%4*138)+690,(item//4*138)+270])
          elif player["inventory"][item]["baseInfo"]["type"] == "hand":
            if player["inventory"][item]["first"] == "tool":
              pygame.draw.polygon(Win,Get_Durability_Color(player["inventory"][item]["durability"][0]/player["inventory"][item]["durability"][1]),[((item%4*138)+689,(item//4*138)+269+128),((item%4*138)+689+(128*(player["inventory"][item]["durability"][0]/player["inventory"][item]["durability"][1])),(item//4*138)+269+128),((item%4*138)+689+(128*(player["inventory"][item]["durability"][0]/player["inventory"][item]["durability"][1])),(item//4*138)+269+127),((item%4*138)+689,(item//4*138)+269+127)])
    Win.blit(Get_Sprite(LO("playerStuff/craftingBox"),(0,0,0),552),(1300,264))
    if player["craftingTool"]["baseInfo"]["type"] == None:
      Draw_Assembley()
      Draw_Assembley_Ingredients(mP)
    elif player["craftingTool"]["second"] == "knife":
      Draw_Carve()
      Draw_Carve_Ingredients(mP)
    Draw_Inv_Item("craftingTool",1507,100)
    Draw_Inv_Item("craftingOutput",1507,850)
    Draw_Inv_Item("leftHand",753,100)
    Draw_Inv_Item("rightHand",1029,100)
    Draw_Inv_Item("helm",509,850)
    Draw_Inv_Item("chest",700,850)
    Draw_Inv_Item("legs",891,850)
    Draw_Inv_Item("boots",1082,850)
    Draw_Inv_Item("gloves",1273,850)

def Draw_Hotbar():
    Win.blit(Get_Sprite(LO("playerStuff/hotbar"),(0,0,0),1068),(426,21))
    if not player["inventory"][0]["baseInfo"]["type"] == None:
      Win.blit(Get_Sprite(player["inventory"][0]["baseInfo"]["itemSprite"],(0,0,0),32),(432,26))
      if player["inventory"][0]["baseInfo"]["type"] == "hand":
        if player["inventory"][0]["first"] == "tool":
          pygame.draw.polygon(Win,Get_Durability_Color(player["inventory"][0]["durability"][0]/player["inventory"][0]["durability"][1]),[(432,58),(432+(32*(player["inventory"][0]["durability"][0]/player["inventory"][0]["durability"][1])),58),(432+(32*(player["inventory"][0]["durability"][0]/player["inventory"][0]["durability"][1])),58),(432,58)])
    if not player["inventory"][1]["baseInfo"]["type"] == None:
      Win.blit(Get_Sprite(player["inventory"][1]["baseInfo"]["itemSprite"],(0,0,0),32),(582,26))
      if player["inventory"][1]["baseInfo"]["type"] == "hand":
        if player["inventory"][1]["first"] == "tool":
          pygame.draw.polygon(Win,Get_Durability_Color(player["inventory"][1]["durability"][0]/player["inventory"][1]["durability"][1]),[(582,58),(582+(32*(player["inventory"][1]["durability"][0]/player["inventory"][1]["durability"][1])),58),(582+(32*(player["inventory"][1]["durability"][0]/player["inventory"][1]["durability"][1])),58),(582,58)])
    if not player["inventory"][2]["baseInfo"]["type"] == None:
      Win.blit(Get_Sprite(player["inventory"][2]["baseInfo"]["itemSprite"],(0,0,0),32),(1305,26))
      if player["inventory"][2]["baseInfo"]["type"] == "hand":
        if player["inventory"][2]["first"] == "tool":
          pygame.draw.polygon(Win,Get_Durability_Color(player["inventory"][2]["durability"][0]/player["inventory"][2]["durability"][1]),[(1305,58),(1305+(32*(player["inventory"][2]["durability"][0]/player["inventory"][2]["durability"][1])),58),(1305+(32*(player["inventory"][2]["durability"][0]/player["inventory"][2]["durability"][1])),58),(1305,58)])
    if not player["inventory"][3]["baseInfo"]["type"] == None:
      Win.blit(Get_Sprite(player["inventory"][3]["baseInfo"]["itemSprite"],(0,0,0),32),(1456,26))
      if player["inventory"][3]["baseInfo"]["type"] == "hand":
        if player["inventory"][3]["first"] == "tool":
          pygame.draw.polygon(Win,Get_Durability_Color(player["inventory"][3]["durability"][0]/player["inventory"][3]["durability"][1]),[(1456,58),(1456+(32*(player["inventory"][3]["durability"][0]/player["inventory"][3]["durability"][1])),58),(1456+(32*(player["inventory"][3]["durability"][0]/player["inventory"][3]["durability"][1])),58),(1456,58)])

def Draw_Stats():
    Win.blit(Get_Sprite(LO("playerStuff/manaStatBar"),(0,0,0),170),(683,21))
    width = int((player["mana"][0]/player["mana"][1])*170)
    pygame.draw.polygon(Win,(0,43,146),[(768-width//2,20),(768+width//2,20),(768+width//2,62),(768-width//2,62)])
    Win.blit(Get_Sprite(LO("playerStuff/hpStatBar"),(0,0,0),170),(875,21))
    width = int((player["hp"][0]/player["hp"][1])*170)
    pygame.draw.polygon(Win,(148,0,0),[(960-width//2,20),(960+width//2,20),(960+width//2,62),(960-width//2,62)])
    Win.blit(Get_Sprite(LO("playerStuff/stamStatBar"),(0,0,0),170),(1067,21))
    width = int((player["stam"][0]/player["stam"][1])*170)
    pygame.draw.polygon(Win,(190,189,0),[(1152-width//2,20),(1152+width//2,20),(1152+width//2,62),(1152-width//2,62)])

def Draw_Hands():
    Win.blit(Get_Sprite(LO("playerStuff/handSlot"),(0,0,0),42),(502,43))
    if not player["leftHand"]["baseInfo"]["type"] == None:
      Win.blit(Get_Sprite(player["leftHand"]["baseInfo"]["itemSprite"],(0,0,0),32),(507,48))
      if player["leftHand"]["baseInfo"]["type"] == "hand":
        if player["leftHand"]["first"] == "tool":
          pygame.draw.polygon(Win,Get_Durability_Color(player["leftHand"]["durability"][0]/player["leftHand"]["durability"][1]),[(507,80),(507+(32*(player["leftHand"]["durability"][0]/player["leftHand"]["durability"][1])),80),(507+(32*(player["leftHand"]["durability"][0]/player["leftHand"]["durability"][1])),80),(507,80)])
    Win.blit(Get_Sprite(LO("playerStuff/handSlot"),(0,0,0),42),(1378,43))
    if not player["rightHand"]["baseInfo"]["type"] == None:
      Win.blit(Get_Sprite(player["rightHand"]["baseInfo"]["itemSprite"],(0,0,0),32),(1383,48))
      if player["rightHand"]["baseInfo"]["type"] == "hand":
        if player["rightHand"]["first"] == "tool":
          pygame.draw.polygon(Win,Get_Durability_Color(player["rightHand"]["durability"][0]/player["rightHand"]["durability"][1]),[(1383,80),(1383+(32*(player["rightHand"]["durability"][0]/player["rightHand"]["durability"][1])),80),(1383+(32*(player["rightHand"]["durability"][0]/player["rightHand"]["durability"][1])),80),(1383,80)])

def Draw_Item_Name(mP,map):
  num = Get_All_Inv_Items(mP,map)
  if isinstance(num,int):
    if num < 16 and not player["inventory"][num]["baseInfo"]["name"] == None:
      Draw_Word(player["inventory"][num]["baseInfo"]["name"],mP)
    elif num == 16 and not player["leftHand"]["baseInfo"]["name"] == None:
      Draw_Word(player["leftHand"]["baseInfo"]["name"],mP)
    elif num == 17 and not player["rightHand"]["baseInfo"]["name"] == None:
      Draw_Word(player["rightHand"]["baseInfo"]["name"],mP)
    elif num == 18 and not player["helm"]["baseInfo"]["name"] == None:
      Draw_Word(player["helm"]["baseInfo"]["name"],mP)
    elif num == 19 and not player["chest"]["baseInfo"]["name"] == None:
      Draw_Word(player["chest"]["baseInfo"]["name"],mP)
    elif num == 20 and not player["legs"]["baseInfo"]["name"] == None:
      Draw_Word(player["legs"]["baseInfo"]["name"],mP)
    elif num == 21 and not player["boots"]["baseInfo"]["name"] == None:
      Draw_Word(player["boots"]["baseInfo"]["name"],mP)
    elif num == 22 and not player["gloves"]["baseInfo"]["name"] == None:
      Draw_Word(player["gloves"]["baseInfo"]["name"],mP)
    elif num == 23 and not player["craftingTool"]["baseInfo"]["name"] == None:
      Draw_Word(player["craftingTool"]["baseInfo"]["name"],mP)
    elif num == 24 and not player["craftingOutput"]["baseInfo"]["name"] == None:
      Draw_Word(player["craftingOutput"]["baseInfo"]["name"],mP)
    elif not player["objectOpen"][0] == None and num > 24:
      object = map[Get_Chunk(player["objectOpen"][0],player["objectOpen"][1],mapChunkSize[0],32)]["chunk"][Get_Square(player["objectOpen"][0],player["objectOpen"][1],32)]["baseBlock"]
      if object["type"] == "storage":
        if not object["inv"][num-25]["baseInfo"]["name"] == None:
          Draw_Word(object["inv"][num-25]["baseInfo"]["name"],mP)

# # # # # #

def Draw_Overlay():
    Draw_Hotbar()
    Draw_Hands()

def Draw_Tab(mP):
    Draw_Inv(mP)
    if not player["heldInvObject"]["item"]["baseInfo"]["type"] == None:
        xy = pygame.mouse.get_pos()
        Win.blit(Get_Sprite(player["heldInvObject"]["item"]["baseInfo"]["invSprite"],(0,0,0),128),(xy[0]-64,xy[1]-64))

###########################################################################################################################################################################################

def Change_Player_Stats():
    if player["stam"][0] < player["stam"][1]:
       player["stam"][0] += 1
    if player["hp"][0] < player["hp"][1]:
       player["hp"][0] += .1
    if player["mana"][0] < player["mana"][1]:
       player["mana"][0] += .5

###################################################################################################################################################################################

def Single_Player_Mode():
    map = Make_Chunks(mapChunkSize[0],mapChunkSize[1])
    itemMap = Make_Item_Chunks(mapChunkSize[0],mapChunkSize[1])
    projectileMap = Make_Projectile_Chunks(mapChunkSize[0],mapChunkSize[1])
    activeBlockMap = Make_Active_Block_Chunks(mapChunkSize[0],mapChunkSize[1])
    tick = 0
    #nextTick = 0
    sec = 0
    beginSec = time()

    while running:
      Win.fill((0,0,0))
      xy = pygame.mouse.get_pos()
      Draw_Screen(map)
      Draw_Screen_Items(itemMap)
      Draw_Active_Screen(activeBlockMap)
      Win.blit(Get_Sprite(player["sprites"][int((Get_Line_Angle([0,0],[xy[0]-960,xy[1]-540])-337.5)//45)],(0,0,0),64),(928,508))
      Get_Keyboard_Events_Single_Player_Mode(map,itemMap,activeBlockMap,sec,tick)
      #Tick_Active_Blocks(sec,activeBlockMap)
      Destroy_Item(sec,itemMap)
      Change_Player_Stats()
      Draw_Stats()
      if invOn:
         Draw_Tab(xy)
         if not player["objectOpen"][0] == None:
           Draw_Open_Object(map)
         Draw_Item_Name([xy[0],xy[1]-10],map)
      else:
         Draw_Overlay()
      tick +=1
      #if sec < int(time()-beginSec):
        #print(tick-nextTick)
        #nextTick = tick
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
        if event.type == pygame.MOUSEBUTTONDOWN and mouseState == "up":
            mouseState = 'down'
        if mouseState == "down":
            mP = pygame.mouse.get_pos()
            mouseState = "down"
        if event.type == pygame.MOUSEBUTTONUP:
            mouseState = 'up'

    Win.blit(Get_Sprite(LO("menu/singlePlayerBanner"),(0,0,0),800),(200,400))
    if mP[0] >= 200 and mP[0] <= 1000 and mP[1] >= 400 and mP[1] <= 600:
      Single_Player_Mode()

    pygame.display.update()