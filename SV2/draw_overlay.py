from stuff import Get_Sprite,LO,Get_Inv_Item_Grid
from items import items
from variables import variables
from crafting import assembely,carving
from get_cs import Get_Chunk,Get_Square
import pygame
from init import Win

def Draw_Word(word,xy):
    total = 0
    for letter in word:
      Win.blit(Get_Sprite(LO(f"LN/{letter}"),(0,0,0),64),[xy[0]+total*6,xy[1]])
      total += 1

def Get_Durability_Color(itemDurability):
    if itemDurability > 0.5:
        return(int(255-(255*((itemDurability-0.5)*2))),255,0)
    if itemDurability < 0.5:
        return(255,int(255*(itemDurability*2)),0)
    if itemDurability == 0.5:
        return(255,255,0)

def Draw_Item(num,x,y,location):
  Win.blit(Get_Sprite(LO("playerStuff/invItem"),(0,0,0),138),[x,y])
  if not location[num]["baseInfo"]["type"] == None:
    Win.blit(Get_Sprite(location[num]["baseInfo"]["invSprite"],(0,0,0),128),[x+5,y+5])
    if location[num]["baseInfo"]["stacks"]:
      stackSize = location[num]["stack"][0]
      Win.blit(Get_Sprite(LO(f"LN/{stackSize}"),(0,0,0),9),[x+6,y+6])
    if location[num]["baseInfo"]["type"] == "hand":
      if location[num]["first"] == "tool":
        pygame.draw.polygon(Win,Get_Durability_Color(location[num]["durability"][0]/location[num]["durability"][1]),[(x+5,y+132),(x+5+(128*(location[num]["durability"][0]/location[num]["durability"][1])),y+132),(x+5+(128*(location[num]["durability"][0]/location[num]["durability"][1])),y+131),(x+5,y+131)])

def Draw_Grid(gridSize,xy,location,num):
    for item in range(gridSize[0]*gridSize[1]):
        Draw_Item(num+item,(item%gridSize[0]*138)+xy[0],(item//gridSize[0]*138)+xy[1],location)

def Draw_Hotbar_Item(num,xy):
    Win.blit(Get_Sprite(LO("playerStuff/handSlot"),(0,0,0),42),(xy[0],xy[1]))
    if not variables["player"][num]["baseInfo"]["type"] == None:
      Win.blit(Get_Sprite(variables["player"][num]["baseInfo"]["itemSprite"],(0,0,0),32),(xy[0]+5,xy[1]+5))
      if variables["player"][num]["baseInfo"]["type"] == "hand":
        if variables["player"][num]["first"] == "tool":
          pygame.draw.polygon(Win,Get_Durability_Color(variables["player"][num]["durability"][0]/variables["player"][num]["durability"][1]),[(xy[0]+5,xy[1]+37),(xy[0]+5+(32*(variables["player"][num]["durability"][0]/variables["player"][num]["durability"][1])),xy[1]+37),(xy[0]+5+(32*(variables["player"][num]["durability"][0]/variables["player"][num]["durability"][1])),xy[1]+37),(xy[0]+5,xy[1]+37)])

def Draw_Item_Name(mP,map,num):
  if isinstance(num,int):
    if num < 25 and not variables["player"][num] == items["none"]:
      Draw_Word(variables["player"][num]["baseInfo"]["name"],mP)
    elif not variables["player"]["objectOpen"][0] == None and num > 24:
      object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
      if not object[num] == items["none"]:
        Draw_Word(object[num]["baseInfo"]["name"],mP)

def Draw_Crafting_Item(name,xy):
   Win.blit(Get_Sprite(LO("playerStuff/invItem"),(0,0,0),138),[xy[0],xy[1]])
   Win.blit(Get_Sprite(LO(f"invView/{name}"),(0,0,0),128),[xy[0]+5,xy[1]+5])

def Draw_Craft(c):
    if c == None:
      for item in range(len(variables["assembelyNames"])):
          Draw_Crafting_Item(variables["assembelyNames"][item],((item%4*138)+1305,(item//4*138)+269))
    elif c == "knife":
      for item in range(len(variables["carvingNames"])):
          Draw_Crafting_Item(variables["carvingNames"][item],((item%4*138)+1305,(item//4*138)+269))

def Draw_Ingredient(name,mp,c):
    total = 0
    for set in c[name]["ingredients"]:
      Draw_Word(name,[mp[0],mp[1]-10])
      Draw_Word(set[0],[mp[0],mp[1]+20+(total*12)])
      Draw_Word(str(set[1]),[mp[0]-16,mp[1]+20+(total*12)])
      total += 1

def Draw_Ingredients(mp,c):
    if c == None:
      num = Get_Inv_Item_Grid([1305,269],[4,4],0,mp,len(variables["assembelyNames"]))
      if not num == None:
         Draw_Ingredient(variables["assembelyNames"][num],mp,assembely)
    elif c == "knife":
      num = Get_Inv_Item_Grid([1305,269],[4,4],0,mp,len(variables["carvingNames"]))
      if not num == None:
         Draw_Ingredient(variables["carvingNames"][num],mp,carving)

def Draw_Open_Object(map):
    object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
    if object["name"] == "Fired_Clay_Pot":
      Draw_Grid([2,2],[211,407],object,25)
    elif object["name"] == "Wood_Chest" or object["name"] == "Reinforced_Wood_Chest":
      Draw_Grid([3,3],[142,338],object,25)
    elif object["name"] == "Iron_Safe" or object["name"] == "Steel_Safe":
      Draw_Grid([4,4],[73,269],object,25)
    elif object["name"] == "Camp_Fire":
      Draw_Grid([2,1],[211,269],object,25)
      Win.blit(Get_Sprite(LO("objectViews/equal"),(0,0,0),64),[317,408])
      Draw_Grid([2,1],[211,476],object,27)
      if object["active"]:
        Win.blit(Get_Sprite(LO("objectViews/fire"),(0,0,0),64),[317,615])
      else:
        Win.blit(Get_Sprite(LO("objectViews/fireOff"),(0,0,0),64),[317,615])
      Draw_Grid([2,1],[211,683],object,29)

def Draw_Inv(mP):
    Draw_Grid([4,4],[689,269],variables["player"],0)
    if variables["player"][23]["baseInfo"]["type"] == None:
      Draw_Craft(None)
      Draw_Ingredients(mP,None)
    elif variables["player"][23]["second"] == "knife":
      Draw_Craft("knife")
      Draw_Ingredients(mP,"knife")
    Draw_Item(16,753,100,variables["player"])
    Draw_Item(17,1029,100,variables["player"])
    Draw_Item(18,509,850,variables["player"])
    Draw_Item(19,700,850,variables["player"])
    Draw_Item(20,891,850,variables["player"])
    Draw_Item(21,1082,850,variables["player"])
    Draw_Item(22,1273,850,variables["player"])
    Draw_Item(23,1507,100,variables["player"])
    Draw_Item(24,1507,850,variables["player"])

def Draw_Hotbar():
    Draw_Hotbar_Item(0,(427,21))
    Draw_Hotbar_Item(1,(577,21))
    Draw_Hotbar_Item(2,(1300,21))
    Draw_Hotbar_Item(3,(1451,21))
    Draw_Hotbar_Item(16,(502,43))
    Draw_Hotbar_Item(17,(1378,43))

def Draw_Stats():
    Win.blit(Get_Sprite(LO("playerStuff/manaStatBar"),(0,0,0),170),(683,21))
    width = int((variables["player"]["mana"][0]/variables["player"]["mana"][1])*170)
    pygame.draw.polygon(Win,(0,43,146),[(768-width//2,20),(768+width//2,20),(768+width//2,62),(768-width//2,62)])
    Win.blit(Get_Sprite(LO("playerStuff/hpStatBar"),(0,0,0),170),(875,21))
    width = int((variables["player"]["hp"][0]/variables["player"]["hp"][1])*170)
    pygame.draw.polygon(Win,(148,0,0),[(960-width//2,20),(960+width//2,20),(960+width//2,62),(960-width//2,62)])
    Win.blit(Get_Sprite(LO("playerStuff/stamStatBar"),(0,0,0),170),(1067,21))
    width = int((variables["player"]["stam"][0]/variables["player"]["stam"][1])*170)
    pygame.draw.polygon(Win,(190,189,0),[(1152-width//2,20),(1152+width//2,20),(1152+width//2,62),(1152-width//2,62)])


def Draw_Tab(mP,map):
    Draw_Inv(mP)
    if not variables["player"]["objectOpen"][0] == None:
           Draw_Open_Object(map)
    if not variables["player"]["heldInvObject"]["item"]["baseInfo"]["type"] == None:
        xy = pygame.mouse.get_pos()
        Win.blit(Get_Sprite(variables["player"]["heldInvObject"]["item"]["baseInfo"]["invSprite"],(0,0,0),128),(xy[0]-64,xy[1]-64))