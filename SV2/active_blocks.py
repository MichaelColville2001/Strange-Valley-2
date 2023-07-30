from items import items,Convert_Item
from item_stuff import Drop_Item
from get_cs import Get_Chunk,Get_Square
from variables import variables

def Use_Fuel(object,nums,itemName,fuelTime):
  for num in nums:
    if object[num]['baseInfo']["name"] == itemName:
      object["active"] = True
      object[num]["stack"][0] -= 1
      object["timeLeft"] = fuelTime
      if object[num]["stack"][0] == 0:
        object[num] = items["none"]
      break

def Cook_Item(object,nums,destination,itemName,cookedTo,cookTime,sec,itemMap,pos):
    for num in nums:
      if object[num]['baseInfo']["name"] == itemName and object["itemTimeLeft"][num] == 0:
        object["itemTimeLeft"][num] = cookTime
      elif object[num]['baseInfo']["name"] == itemName and object["itemTimeLeft"][num] <= sec: #cooks
        placed = False
        for item in range(len(destination)):
          if object[num]['baseInfo']["stacks"]:
            object[num]["stack"][0] -= 1
            if object[destination[item]] == items["none"]:
              object[destination[item]] = Convert_Item(items[cookedTo])
              if object[num]["stack"][0] == 0:
                object[num] = items["none"]
                object["itemTimeLeft"][num] = 0
                placed = True
                break
              elif not object[num]["stack"][0] == 0:
                object["itemTimeLeft"][num] = cookTime
                placed = True
                break
            if object[destination[item]]['baseInfo']["name"] == object[num]['baseInfo']["name"] and object[destination[item]]["stack"][0] < object[destination[item]]["stack"][1]:
              object[destination[item]]["stack"][0] += 1
              if object[num]["stack"][0] == 0:
                object[num] = items["none"]
                object["itemTimeLeft"][num] = 0
                placed = True
                break
              elif not object[num]["stack"][0] == 0:
                object["itemTimeLeft"][num] = cookTime
                placed = True
                break
          elif not object[num]['baseInfo']["stacks"]:
            if object[destination[item]] == items["none"]:
              object[destination[item]] = Convert_Item(items[cookedTo])
              object[num] = items["none"]
              object["itemTimeLeft"][num] = 0
              placed = True
              break
        if not placed:
          Drop_Item(pos,itemMap,Convert_Item(items[cookedTo]),sec,[64,64])
          object[num] = items["none"]
      

def Tick_Active_Blocks(sec,activeBlockMap,map,itemMap):
    for block in range(len(activeBlockMap)):
      object = map[Get_Chunk(activeBlockMap[block][0],activeBlockMap[block][1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(activeBlockMap[block][0],activeBlockMap[block][1],32)]["baseBlock"]
      pos = [activeBlockMap[block][0]*64,activeBlockMap[block][1]*64]
      if object["name"] == "Camp_Fire":
        if object["timeLeft"] <= sec:
           object["active"] = False
        if not object["active"]:
          Use_Fuel(object,[29,30],"Log",sec+60)
          if not object["active"]:
            object["itemTimeLeft"][27] = 0
            object["itemTimeLeft"][28] = 0
        if object["active"]:
          Cook_Item(object,[27,28],[25,26],"Clay_Pot","Fired_Clay_Pot",5+sec,sec,itemMap,pos)
          #Cook_Item(object,[27,28],[25,26],"Clay_Brick","Fired_Clay_Brick",5+sec,sec,itemMap,pos)
          #Cook_Item(object,[27,28],[25,26],"Clay_Ingot_Mould","Fired_Clay_Ingot_Mould",5+sec,sec,itemMap,pos)
          #Cook_Item(object,[27,28],[25,26],"Clay_Axe_Head_Mould","Fired_Clay_Axe_Head_Mould",5+sec,sec,itemMap,pos)
          #Cook_Item(object,[27,28],[25,26],"Clay_Pick_Head_Mould","Fired_Clay_Pick_Head_Mould",5+sec,sec,itemMap,pos)
          #Cook_Item(object,[27,28],[25,26],"Clay_Hammer_Head_Mould","Fired_Clay_Hammer_Head_Mould",5+sec,sec,itemMap,pos)
          #Cook_Item(object,[27,28],[25,26],"Clay_Knife_Blade_Mould","Fired_Clay_Knife_Blade_Mould",5+sec,sec,itemMap,pos)
          #Cook_Item(object,[27,28],[25,26],"Log","Charcoal",5+sec,sec,itemMap,pos)
