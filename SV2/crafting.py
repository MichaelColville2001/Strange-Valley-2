from items import items,Convert_Item
from variables import variables
from stuff import Get_Inv_Item_Grid

assembely ={"Stone_Knife":{"ingredients":[["Stone",2]]},
            "Stone_Axe":{"ingredients":[["Primitive_Wood_Axe_Handle",1],["Stone_Knife",1]]},
            "Camp_Fire":{"ingredients":[["Stone",8]]},
            "Clay_Pot":{"ingredients":[["Clay",4]]}}


carving = {"Pry_Stick":{"tier":0,"work":1,"ingredients":[["Log",1]]},
           "Primitive_Wood_Axe_Handle":{"tier":0,"work":1,"ingredients":[["Log",1]]}}


#########################################################################################################################################################################################

def Check_For_Item(item,itemAmount):
  total = itemAmount
  item = items[item]
  for num in range(16):
    if variables["player"][num]["baseInfo"]["name"] == item["baseInfo"]["name"]:
      if item["baseInfo"]["stacks"]:
        total -= variables["player"][num]["stack"][0]
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
  if variables["player"][23]["durability"][0] >= carving[craftingItem]["work"] and variables["player"][23]["tier"] >= carving[craftingItem]["tier"]:
    for items in range(len(carving[craftingItem]["ingredients"])):
      if not Check_For_Item(carving[craftingItem]["ingredients"][items][0],carving[craftingItem]["ingredients"][items][1]):
        return False
    return True
  else:
    return False

def Assemble(craftingItem):
  if variables["player"][24]["baseInfo"]["type"] == None:
    if Can_Assemble(craftingItem):
      for objects in range(len(assembely[craftingItem]["ingredients"])):
        item = items[assembely[craftingItem]["ingredients"][objects][0]]
        amount = assembely[craftingItem]["ingredients"][objects][1]
        if item["baseInfo"]["stacks"]:
          for num in range(16):
            if amount == 0:
              break
            if item["baseInfo"]["name"] == variables["player"][num]["baseInfo"]["name"]:
              if (amount - variables["player"][num]["stack"][0]) >= 0:
                amount -= variables["player"][num]["stack"][0]
                variables["player"][num] = items["none"]
              elif (amount - variables["player"][num]["stack"][0]) < 0:
                variables["player"][num]["stack"][0] -= amount
                amount = 0
        else:
          for num in range(16):
            if amount == 0:
              break
            if item["baseInfo"]["name"] == variables["player"][num]["baseInfo"]["name"]:
                variables["player"][num] = items["none"]
                amount -= 1
      variables["player"][24] = Convert_Item(items[craftingItem])

def Carve(craftingItem):
  if variables["player"][24]["baseInfo"]["type"] == None:
    if Can_Carve(craftingItem):
      for objects in range(len(carving[craftingItem]["ingredients"])):
        item = items[carving[craftingItem]["ingredients"][objects][0]]
        amount = carving[craftingItem]["ingredients"][objects][1]
        if item["baseInfo"]["stacks"]:
          for num in range(16):
            if amount == 0:
              break
            if item["baseInfo"]["name"] == variables["player"][num]["baseInfo"]["name"]:
              if (amount - variables["player"][num]["stack"][0]) >= 0:
                amount -= variables["player"][num]["stack"][0]
                variables["player"][num] = items["none"]
              elif (amount - variables["player"][num]["stack"][0]) < 0:
                variables["player"][num]["stack"][0] -= amount
                amount = 0
        else:
          for num in range(16):
            if amount == 0:
              break
            if item["baseInfo"]["name"] == variables["player"][num]["baseInfo"]["name"]:
                variables["player"][num] = items["none"]
                amount -= 1
      variables["player"][23]["durability"][0] -= carving[craftingItem]["work"]
      if variables["player"][23]["durability"][0] == 0:
        variables["player"][23] = items["none"]
      variables["player"][24] = Convert_Item(items[craftingItem])

def Get_Assemble_Items(mP):
    num = Get_Inv_Item_Grid([1305,269],[4,4],0,mP,len(variables["assembelyNames"]))
    if not num == None:
      Assemble(variables["assembelyNames"][num])

def Get_Carve_Items(mP):
    num = Get_Inv_Item_Grid([1305,269],[4,4],0,mP,len(variables["carvingNames"]))
    if not num == None:
      Carve(variables["carvingNames"][num])