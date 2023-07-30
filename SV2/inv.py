from variables import variables
from items import items,Convert_Item
from item_stuff import Drop_Held_Item,Drop_Item
from get_cs import Get_Square,Get_Chunk
from random import randint
import pygame


def Hotbar_Quick_Change(num,hand):
    if variables["player"][num]["baseInfo"]["type"] == "hand" or variables["player"][num]["baseInfo"]["type"] == None:
      temp = variables["player"][num]
      variables["player"][num] = variables["player"][hand]
      variables["player"][hand] = temp

def Basic_Put_Back(sec,itemMap,location):
    if location[variables["player"]["heldInvObject"]["index"]] == items["none"]:
      location[variables["player"]["heldInvObject"]["index"]] = variables["player"]["heldInvObject"]["item"]
      variables["player"]["heldInvObject"]["item"] = items["none"]
    elif location[variables["player"]["heldInvObject"]["index"]]["baseInfo"] == variables["player"]["heldInvObject"]["item"]["baseInfo"]:
      if location[variables["player"]["heldInvObject"]["index"]]["stack"][0] < location[variables["player"]["heldInvObject"]["index"]]["stack"][1]:
        if location[variables["player"]["heldInvObject"]["index"]]["stack"][0] + variables["player"]["heldInvObject"]["item"]["stack"][0] <= location[variables["player"]["heldInvObject"]["index"]]["stack"][1]:
          location[variables["player"]["heldInvObject"]["index"]]["stack"][0] += variables["player"]["heldInvObject"]["item"]["stack"][0]
          variables["player"]["heldInvObject"]["item"] = items["none"]
        elif location[variables["player"]["heldInvObject"]["index"]]["stack"][0] + variables["player"]["heldInvObject"]["item"]["stack"][0] > location[variables["player"]["heldInvObject"]["index"]]["stack"][1]:
          change = location[variables["player"]["heldInvObject"]["index"]]["stack"][1] - location[variables["player"]["heldInvObject"]["index"]]["stack"][0]
          location[variables["player"]["heldInvObject"]["index"]]["stack"][0] = location[variables["player"]["heldInvObject"]["index"]]["stack"][1]
          variables["player"]["heldInvObject"]["item"]["stack"][0] -= change
        else:
          Drop_Held_Item(sec,itemMap)
      else:
        Drop_Held_Item(sec,itemMap)

def Put_Back(sec,itemMap,map):
    if variables["player"]["heldInvObject"]["index"] < 25:
      Basic_Put_Back(sec,itemMap,variables["player"])
    elif variables["player"]["heldInvObject"]["index"] > 24:
      object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
      Basic_Put_Back(sec,itemMap,object)
    else:
      Drop_Held_Item(sec,itemMap)

def Basic_Place_Stack(location,num,sec,itemMap,map):
    if location[num]["stack"][0] < location[num]["stack"][1]:
      if location[num]["stack"][0] + variables["player"]["heldInvObject"]["item"]["stack"][0] <= location[num]["stack"][1]:
        location[num]["stack"][0] += variables["player"]["heldInvObject"]["item"]["stack"][0]
        variables["player"]["heldInvObject"]["item"] = items["none"]
      else:
        change = location[num]["stack"][1] - location[num]["stack"][0]
        location[num]["stack"][0] = location[num]["stack"][1]
        variables["player"]["heldInvObject"]["item"]["stack"][0] -= change
        Put_Back(sec,itemMap,map)
    else:
      Put_Back(sec,itemMap,map)

def Place_Stack(num,sec,itemMap,map):
  if num < 25:
    Basic_Place_Stack(variables["player"],num,sec,itemMap,map)
  elif num > 24:
    object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
    Basic_Place_Stack(object,num,sec,itemMap,map)

def Check(num,map,item):
    if num < 16:
      return True
    elif (num == 16 or num == 17) and item["baseInfo"]["type"] == "hand":
      return True
    elif num == 18 and item["baseInfo"]["type"] == "helm":
      return True
    elif num == 19 and item["baseInfo"]["type"] == "chest":
      return True
    elif num == 20 and item["baseInfo"]["type"] == "legs":
      return True
    elif num == 21 and item["baseInfo"]["type"] == "boots":
      return True
    elif num == 22 and item["baseInfo"]["type"] == "gloves":
      return True
    elif num == 23 and item["baseInfo"]["type"] == "hand":
      if item["second"] == "knife":
        return True
      else:
        return False
    if num > 24: 
      object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
      if object["type"] == "storage":
        return True
      elif object["type"] == "foodCooker":
        if num == 27 or num == 28:
          if item["baseInfo"]["name"] == "Clay" or "Clay_Pot":
            return True
        if num == 29 or num == 30:
          if item["baseInfo"]["name"] == "Log":
            return True
    else:
      return False

def Basic_Place(location1,location2,num,map,sec,itemMap):
    if location1[num] == items["none"]:
      if Check(num,map,variables["player"]["heldInvObject"]["item"]):
        location1[num] = variables["player"]["heldInvObject"]["item"]
        variables["player"]["heldInvObject"]["item"] = items["none"]
      else:
        Put_Back(sec,itemMap,map)
    elif not location1[num] == items["none"] and location2[variables["player"]["heldInvObject"]["index"]] == items["none"]:
      if location1[num]["baseInfo"] == variables["player"]["heldInvObject"]["item"]["baseInfo"] and location1[num]["baseInfo"]["stacks"]:
        Place_Stack(num,sec,itemMap,map)
      elif Check(num,map,variables["player"]["heldInvObject"]["item"]) and Check(variables["player"]["heldInvObject"]["index"],map,location1[num]):
        location2[variables["player"]["heldInvObject"]["index"]] = location1[num]
        location1[num] = variables["player"]["heldInvObject"]["item"]
        variables["player"]["heldInvObject"]["item"] = items["none"]
      else:
        Put_Back(sec,itemMap,map)
    elif not location1[num] == items["none"] and not location2[variables["player"]["heldInvObject"]["index"]] == items["none"] and (location1[num]["baseInfo"] == variables["player"]["heldInvObject"]["item"]["baseInfo"] and location1[num]["baseInfo"]["stacks"]):
      Place_Stack(num,sec,itemMap,map)

    else:
        Put_Back(sec,itemMap,map)

def Place(num,map,sec,itemMap):
  if num < 24 and variables["player"]["heldInvObject"]["index"] < 25: #inv to inv
    Basic_Place(variables["player"],variables["player"],num,map,sec,itemMap)
  elif num < 24 and variables["player"]["heldInvObject"]["index"] > 24: #object to inv
    object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
    Basic_Place(variables["player"],object,num,map,sec,itemMap)
  elif num > 24 and variables["player"]["heldInvObject"]["index"] < 25: #inv to object
    object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
    Basic_Place(object,variables["player"],num,map,sec,itemMap)
  elif num > 24 and variables["player"]["heldInvObject"]["index"] > 24: #object to object
    object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
    Basic_Place(object,object,num,map,sec,itemMap)
  else:
        Put_Back(sec,itemMap,map)

def Up_Click(num,map,sec,itemMap):
  if not variables["player"]["heldInvObject"]["item"] == items["none"]:
    Place(num,map,sec,itemMap)

##############################################################################################################################################################################################

def Pick_Up(num):
      variables["player"]["heldInvObject"]["item"] = variables["player"][num] 
      variables["player"][num] = items["none"]
      variables["player"]["heldInvObject"]["index"] = num

def Object_Pick_Up(num,map):
      object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
      variables["player"]["heldInvObject"]["item"] = object[num] 
      object[num]  = items["none"]
      variables["player"]["heldInvObject"]["index"] = num
        
def Half_Stack(num):
  stackSize = variables["player"][num]["stack"][0]
  if stackSize % 2 == 0:
    variables["player"]["heldInvObject"]["item"] = Convert_Item(variables["player"][num])
    variables["player"]["heldInvObject"]["item"]["stack"][0] = stackSize//2
    variables["player"][num]["stack"][0] = stackSize//2
    variables["player"]["heldInvObject"]["index"] = num
  elif stackSize % 2 == 1:
    variables["player"]["heldInvObject"]["item"] = Convert_Item(variables["player"][num])
    variables["player"]["heldInvObject"]["item"]["stack"][0] = stackSize//2
    variables["player"][num]["stack"][0] = stackSize//2 + 1
    variables["player"]["heldInvObject"]["index"] = num

def Half_Stack_Object(num,map):
    object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
    if object[num]["baseInfo"]["stacks"]:
      if not object[num]["stack"][0] == 1:
        stackSize = object[num]["stack"][0]
        if stackSize % 2 == 0:
          variables["player"]["heldInvObject"]["item"] = Convert_Item(object[num])
          variables["player"]["heldInvObject"]["item"]["stack"][0] = stackSize//2
          object[num]["stack"][0] = stackSize//2
          variables["player"]["heldInvObject"]["index"] = num
        elif stackSize % 2 == 1:
          variables["player"]["heldInvObject"]["item"] = Convert_Item(object[num])
          variables["player"]["heldInvObject"]["item"]["stack"][0] = stackSize//2
          object[num]["stack"][0] = stackSize//2 + 1
          variables["player"]["heldInvObject"]["index"] = num

def Remove_One(num):
  variables["player"]["heldInvObject"]["item"] = Convert_Item(variables["player"][num])
  variables["player"]["heldInvObject"]["item"]["stack"][0] = 1
  variables["player"][num]["stack"][0] -= 1
  variables["player"]["heldInvObject"]["index"] = num

def Remove_One_Object(num,map):
  object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
  if object[num]["baseInfo"]["stacks"]:
    if not object[num]["stack"][0] == 1:
      variables["player"]["heldInvObject"]["item"] = Convert_Item(object[num])
      variables["player"]["heldInvObject"]["item"]["stack"][0] = 1
      object[num]["stack"][0] -= 1
      variables["player"]["heldInvObject"]["index"] = num

#########################################################################################################################################################################################

def Tab_Switch(num,type,mP,itemMap,sec,shift,map):
  if type == 0:
    if variables["leftRightMouseButton"][0] and not shift:  
      if isinstance(num,int):
        if num < 25:
          Pick_Up(num)
        elif not variables["player"]["objectOpen"][0] == None and num > 24:
          Object_Pick_Up(num,map)

    elif variables["leftRightMouseButton"][2] and not shift: 
      if isinstance(num,int):
        if num < 18 and variables["player"][num]["baseInfo"]["stacks"]:
          if not variables["player"][num]["stack"][0] == 1:
            Half_Stack(num)
        elif not variables["player"]["objectOpen"][0] == None and num > 24:
          Half_Stack_Object(num,map)

    elif (variables["leftRightMouseButton"][2] or variables["leftRightMouseButton"][0]) and shift: 
      if isinstance(num,int):
        if num < 18 and variables["player"][num]["baseInfo"]["stacks"]:
          if not variables["player"][num]["stack"][0] == 1:
            Remove_One(num)
        elif not variables["player"]["objectOpen"][0] == None and num > 24:
            Remove_One_Object(num,map)

  if type == 1:
    if isinstance(num,int):
      Up_Click(num,map,sec,itemMap)
    else:
      mP = pygame.mouse.get_pos()
      Drop_Item((mP[0]+variables["relativePerspective"][0]-16,mP[1]+variables["relativePerspective"][1]-16),itemMap,variables["player"]["heldInvObject"]["item"],sec,[32,32])
      variables["player"]["heldInvObject"]["item"] = items["none"]

def Can_Hold_None_Stacked(location,sec,itemMap):
    for num in range(16):
      if variables["player"][num] == items["none"]:
        variables["player"][num] = variables["player"][location]
        variables["player"][location] = items["none"]
        break
    Drop_Item((variables["player"]["position"][0]*64+randint(-16,16),variables["player"]["position"][1]*64+randint(-16,16)),itemMap,variables["player"][location],sec,[64,64])
    variables["player"][location] = items["none"]

def Can_Hold_Stacked(location,sec,itemMap):
    for num in range(16):
      if variables["player"][num]["baseInfo"] == variables["player"][location]["baseInfo"]:
        if variables["player"][location]["stack"][0] + variables["player"][num]["stack"][0] <= variables["player"][num]["stack"][1]:
          object = variables["player"][num]["stack"][0] + variables["player"][location]["stack"][0]
          variables["player"][num]["stack"][0] = object
          variables["player"][location] = items["none"]
          break
        else:
          change = variables["player"][num]["stack"][1] - variables["player"][num]["stack"][0]
          variables["player"][num]["stack"][0] = variables["player"][num]["stack"][1]
          variables["player"][location]["stack"][0] -= change
    for num in range(16):
      if variables["player"][num] == items["none"]:
        variables["player"][num] = variables["player"][location]
        variables["player"][location] = items["none"]
        break
    Drop_Item((variables["player"]["position"][0]*64+randint(-16,16),variables["player"]["position"][1]*64+randint(-16,16)),itemMap,variables["player"][location],sec,[64,64])
    variables["player"][location] = items["none"]

def Close_Inv(sec,itemMap,map):
    if not variables["player"]["heldInvObject"]["item"] == items["none"]:
      if not variables["player"]["heldInvObject"]["item"]["baseInfo"]["stacks"]:
        Put_Back(sec,itemMap,map)
      else:
        if variables["player"]["heldInvObject"]["index"] < 24:
          Put_Back(sec,itemMap,map)
    if not variables["player"][23] == items["none"]:
      if not variables["player"][23]["baseInfo"]["stacks"]:
        Can_Hold_None_Stacked(23,sec,itemMap)
      else:
        Can_Hold_Stacked(23,sec,itemMap)
    if not variables["player"][24] == items["none"]:
      if not variables["player"][24]["baseInfo"]["stacks"]:
        Can_Hold_None_Stacked(24,sec,itemMap)
      else:
        Can_Hold_Stacked(24,sec,itemMap)