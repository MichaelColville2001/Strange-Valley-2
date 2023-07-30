from stuff import Get_Inv_Item_Grid
from variables import variables
from get_cs import Get_Chunk,Get_Square

def Get_4_Storage(mP):
    num = Get_Inv_Item_Grid([211,407],[2,2],25,mP,4)
    return num

def Get_9_Storage(mP):
    num = Get_Inv_Item_Grid([142,338],[3,3],25,mP,9)
    return num

def Get_16_Storage(mP):
    num = Get_Inv_Item_Grid([73,269],[4,4],25,mP,16)
    return num

def Get_Camp_Fire(mP):
    num = Get_Inv_Item_Grid([211,269],[2,1],25,mP,2)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([211,476],[2,1],27,mP,2)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([211,683],[2,1],29,mP,2)
    if not num == None:
       return num 
    else:
       return None
    
def Get_Inv(mP):
    num = Get_Inv_Item_Grid([689,269],[4,4],0,mP,16)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([753,100],[1,1],16,mP,1)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([1029,100],[1,1],17,mP,1)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([509,850],[1,1],18,mP,1)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([700,850],[1,1],19,mP,1)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([891,850],[1,1],20,mP,1)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([1082,850],[1,1],21,mP,1)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([1273,850],[1,1],22,mP,1)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([1507,100],[1,1],23,mP,1)
    if not num == None:
       return num 
    num = Get_Inv_Item_Grid([1507,850],[1,1],24,mP,1)
    if not num == None:
       return num 
    else:
       return None
    

def Get_All_Inv_Items(mP,map):
    num = Get_Inv(mP)
    if not variables["player"]["objectOpen"][0] == None:
      object = map[Get_Chunk(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(variables["player"]["objectOpen"][0],variables["player"]["objectOpen"][1],32)]["baseBlock"]
      if object["name"] == "Fired_Clay_Pot" and isinstance(Get_4_Storage(mP),int):
        num = Get_4_Storage(mP)
        return num
      elif (object["name"] == "Wood_Chest" or object["name"] == "Reinforced_Wood_Chest") and isinstance(Get_9_Storage(mP),int):
        num = Get_9_Storage(mP)
        return num
      elif (object["name"] == "Iron_Safe" or object["name"] == "Steel_Safe") and isinstance(Get_16_Storage(mP),int):
        num = Get_16_Storage(mP)
        return num
      elif object["name"] == "Camp_Fire" and isinstance(Get_Camp_Fire(mP),int):
        num = Get_Camp_Fire(mP)
        return num
      else:
        return num
    else:
      return num