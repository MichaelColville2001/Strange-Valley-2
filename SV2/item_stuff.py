from get_cs import Get_Chunk
from variables import variables
from items import items
from stuff import Dist
from random import randint
from init import WIDTH,HEIGHT

def Drop_Item(pos,itemMap,item,sec,size):
    if not item["baseInfo"]["type"] == None: 
      posX = pos[0]+(size[0]/2)-16
      posY = pos[1]+(size[1]/2)-16
      itemMap[Get_Chunk(int(posX/64),int(posY/64),variables["mapChunkSize"][0],32)]["chunk"].append({"position":[posX,posY],"timeLeft":sec+300,"item":item})

def Item_Pick_Up_Non_Stacked(chunk,item):
  if Dist(chunk["chunk"][item]["position"][0],chunk["chunk"][item]["position"][1],variables["player"]["position"][0]*64,variables["player"]["position"][1]*64) < 75:
    for num in range(16):
      if variables["player"][num] == items["none"]:
        variables["player"][num] = chunk["chunk"][item]["item"]
        chunk["chunk"].pop(item)
        return -1
    return 0
  return 0

def Item_Pick_Up_Stacked(chunk,item):
  if Dist(chunk["chunk"][item]["position"][0],chunk["chunk"][item]["position"][1],variables["player"]["position"][0]*64,variables["player"]["position"][1]*64) < 75:
    for num in range(16):
      if variables["player"][num]["baseInfo"] == chunk["chunk"][item]["item"]["baseInfo"]:
        if chunk["chunk"][item]["item"]["stack"][0] + variables["player"][num]["stack"][0] <= variables["player"][num]["stack"][1]:
          object = variables["player"][num]["stack"][0] + chunk["chunk"][item]["item"]["stack"][0]
          variables["player"][num]["stack"][0] = object
          chunk["chunk"].pop(item)
          return -1
        else:
          change = variables["player"][num]["stack"][1] - variables["player"][num]["stack"][0]
          variables["player"][num]["stack"][0] = variables["player"][num]["stack"][1]
          chunk["chunk"][item]["item"]["stack"][0] -= change
    for num in range(16):
      if variables["player"][num] == items["none"]:
        variables["player"][num] = chunk["chunk"][item]["item"]
        chunk["chunk"].pop(item)
        return -1
    return 0
  return 0

def Pick_up_item(chunk):
  minus = 0
  if len(chunk["chunk"]) > 0:
      for item in range(len(chunk["chunk"])):
        if chunk["chunk"][item+minus]["position"][0]-variables["relativePerspective"][0] >= -32 and chunk["chunk"][item+minus]["position"][0]-variables["relativePerspective"][0] <= WIDTH and chunk["chunk"][item+minus]["position"][1]-variables["relativePerspective"][1] >= -32 and chunk["chunk"][item+minus]["position"][1]-variables["relativePerspective"][1] <= HEIGHT:
          if chunk["chunk"][item+minus]["item"]["baseInfo"]["stacks"] == False:
            minus += Item_Pick_Up_Non_Stacked(chunk,item+minus)
          elif chunk["chunk"][item+minus]["item"]["baseInfo"]["stacks"] == True:
            minus += Item_Pick_Up_Stacked(chunk,item+minus)

def Drop_Held_Item(sec,itemMap):
    Drop_Item((variables["player"]["position"][0]*64+randint(-16,16),variables["player"]["position"][1]*64+randint(-16,16)),itemMap,variables["player"]["heldInvObject"]["item"],sec,[64,64])
    variables["player"]["heldInvObject"]["item"] = items["none"]

def Destroy_Item(sec,itemMap):
    for chunk in range(len(itemMap)):
      for item in range(len(itemMap[chunk]["chunk"])):
        if itemMap[chunk]["chunk"][item]["timeLeft"] == sec:
           itemMap[chunk]["chunk"].pop(item)