from random import randint
from variables import variables
from get_cs import Get_Chunk_Clicked,Get_Square_Clicked,Get_Square_Cord,Check_If_Block_Pix
from stuff import Dist
from item_stuff import Drop_Item
from items import items,Convert_Item
from blocks import baseBlocks,Convert_Blocks

def Pick_Loot(list):
    item = list[(randint(1,len(list))-1)]
    return Convert_Item(item)

def Destroy_Block(mP,hand,map,itemMap,sec,blockType):
  object = map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]
  if not object["baseBlock"]["type"] == None:
    if object["baseBlock"]["type"] == blockType and variables["player"][hand]["tier"] >= object["baseBlock"]["tier"] and Dist(object["position"][0],object["position"][1],variables["player"]["position"][0],variables["player"]["position"][1]) <= 4:
      variables["player"][hand]["durability"][0] -= 1
      map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"][0] -= variables["player"][hand]["damage"]*object["baseBlock"]["resistance"]
      if variables["player"][hand]["durability"][0] <= 0:
        variables["player"][hand] = items["none"]
      if map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"][0] <= 0:
        for item in range(object["baseBlock"]["dropTable"][1]):
          Drop_Item((object["position"][0]*64+randint(-16,16),object["position"][1]*64+randint(-16,16)),itemMap,Pick_Loot(object["baseBlock"]["dropTable"][0]),sec,[64,64]) 
        map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"] = baseBlocks["none"]
    elif object["baseBlock"]["tier"] <= 0  and Dist(object["position"][0],object["position"][1],variables["player"]["position"][0],variables["player"]["position"][1]) <= 4:
      map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"][0] -= 1*object["baseBlock"]["resistance"]
      if map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["hp"][0] <= 0:
        for item in range(object["baseBlock"]["dropTable"][1]):
          Drop_Item((object["position"][0]*64+randint(-16,16),object["position"][1]*64+randint(-16,16)),itemMap,Pick_Loot(object["baseBlock"]["dropTable"][0]),sec,[64,64]) 
        map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"] = baseBlocks["none"]

##################################################################################################################################################################################3

def Place_Block(mP,hand,map,activeMap):
  blockPos = Get_Square_Cord(mP[0],mP[1])
  if Dist(variables["player"]["position"][0],variables["player"]["position"][1],blockPos[0],blockPos[1]) <=4:
      if not Check_If_Block_Pix(map,mP):
        if variables["player"][hand]["second"] == "active":
          item = Convert_Blocks(baseBlocks[variables["player"][hand]["baseInfo"]["name"]])
          position = [blockPos[0],blockPos[1]]
          activeMap.append(position)
          map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,mP[0],mP[1])]["baseBlock"] = item
          variables["player"][hand] = items["none"]
        elif variables["player"][hand]["second"] == "inActive":
          item = Convert_Blocks(baseBlocks[variables["player"][hand]["baseInfo"]["name"]])
          map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,mP[0],mP[1])]["baseBlock"] = item
          variables["player"][hand] = items["none"]