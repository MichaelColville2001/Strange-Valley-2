import pygame
from stuff import LO,Drop_Table,Get_Line_Angle
from items import items
from random import randint

floorBlocks = {"Grass": {"name":"Grass","blockType":"floor","type":"grass","sprites":[LO("floorBlocks/grass1"),LO("floorBlocks/grass2"),LO("floorBlocks/grass3"),LO("floorBlocks/grass4")]},
               "Water": {"name":"Water","blockType":"floor","type":"water","sprites":[LO("floorBlocks/water")]},
               "Dirt": {"name":"Dirt","blockType":"floor","type":"dirt","sprites":[LO("floorBlocks/dirt")]}}

# # # # #

baseBlocks = {"none":{"name":None,"blockType":"base","type":None,"sprites":None},
              
              "Rock":{"name":"Rock","blockType":"base","type":"rock","sprites":[LO("baseBlocks/rock")],"tier":2,"hp":[100,100],"resistance":0.95,"dropTable":[Drop_Table(items["Stone"],1),5]},
              "Log":{"name":"Log","blockType":"base","type":"wood","sprites":[LO("baseBlocks/wood")],"tier":1,"hp":[100,100],"resistance":0.95,"dropTable":[Drop_Table(items["Log"],1),5]},

              "Rock_Pile":{"name":"Rock_Pile","blockType":"pile","type":"rock","sprites":[LO("baseBlocks/rockPile1"),LO("baseBlocks/rockPile2"),LO("baseBlocks/rockPile3"),LO("baseBlocks/rockPile4")],"tier":0,"hp":[100,100],"resistance":1,"dropTable":[Drop_Table(items["Stone"],2,items["Clay"],2),10]},

              "Bush":{"name":"Bush","blockType":"plant","type":"wood","sprites":[LO("baseBlocks/bush")],"tier":0,"hp":[100,100],"resistance":1,"dropTable":[Drop_Table(items["Log"],2,items["none"],1),5]},
              
              # # # # #

              "Clay_Brick_Wall":{"name":"Clay_Brick_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":1,"hp":[100,100],"resistance":0.95},
              "Adobe_Wall":{"name":"Adobe_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":1,"hp":[100,100],"resistance":0.95},
              "Wood_Wall":{"name":"Wood_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":2,"hp":[100,100],"resistance":0.95},
              "Reinforced_Wood_Wall":{"name":"Reinforced_Wood_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":3,"hp":[100,100],"resistance":0.95},
              "Stone_Wall":{"name":"Stone_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":4,"hp":[100,100],"resistance":0.95},
              "Reinforced_Concrete_Wall":{"name":"Reinforced_Concrete_Wall","blockType":"inActive","type":"wall","sprite":None,"tier":5,"hp":[100,100],"resistance":0.95},

              # # # # #

              "Fired_Clay_Pot":{"name":"Fired_Clay_Pot","blockType":"inActive","type":"storage","sprites":LO("inActiveBlocks/firedClayPot"),"tier":1,"hp":[100,100],"resistance":0.95,25:items["none"],26:items["none"],27:items["none"],28:items["none"]},
              "Wood_Chest":{"name":"Wood_Chest","blockType":"inActive","type":"storage","sprites":[LO("inActiveBlocks/woodChest3"),LO("inActiveBlocks/woodChest4"),LO("inActiveBlocks/woodChest1"),LO("inActiveBlocks/woodChest2")],"tier":2,"hp":[100,100],"resistance":0.95,25:items["none"],26:items["none"],27:items["none"],28:items["none"],29:items["none"],30:items["none"],31:items["none"],32:items["none"],33:items["none"]},
              "Reinforced_Wood_Chest":{"name":"Reinforced_Wood_Chest","blockType":"inActive","type":"storage","sprites":[LO("inActiveBlocks/reinforcedWoodChest3"),LO("inActiveBlocks/reinforcedWoodChest4"),LO("inActiveBlocks/reinforcedWoodChest1"),LO("inActiveBlocks/reinforcedWoodChest2")],"tier":3,"hp":[100,100],"resistance":0.95,25:items["none"],26:items["none"],27:items["none"],28:items["none"],29:items["none"],30:items["none"],31:items["none"],32:items["none"],33:items["none"]},
              "Iron_Safe":{"name":"Iron_Safe","blockType":"inActive","type":"storage","sprites":[LO("inActiveBlocks/ironSafe3"),LO("inActiveBlocks/ironSafe4"),LO("inActiveBlocks/ironSafe1"),LO("inActiveBlocks/ironSafe2")],"tier":4,"hp":[100,100],"resistance":0.95,25:items["none"],26:items["none"],27:items["none"],28:items["none"],29:items["none"],30:items["none"],31:items["none"],32:items["none"],33:items["none"],34:items["none"],35:items["none"],36:items["none"],37:items["none"],38:items["none"],39:items["none"],40:items["none"]},
              "Steel_Safe":{"name":"Steel_Safe","blockType":"inActive","type":"storage","sprites":[LO("inActiveBlocks/steelSafe3"),LO("inActiveBlocks/steelSafe4"),LO("inActiveBlocks/steelSafe1"),LO("inActiveBlocks/steelSafe2")],"tier":5,"hp":[100,100],"resistance":0.95,25:items["none"],26:items["none"],27:items["none"],28:items["none"],29:items["none"],30:items["none"],31:items["none"],32:items["none"],33:items["none"],34:items["none"],35:items["none"],36:items["none"],37:items["none"],38:items["none"],39:items["none"],40:items["none"]},
              
              # # # # #

              "Camp_Fire":{"name":"Camp_Fire","blockType":"active","type":"foodCooker","active":False,"onSprite":LO("activeBlocks/onCampFire"),"offSprite":LO("activeBlocks/offCampFire"),25:items["none"],26:items["none"],27:items["none"],28:items["none"],29:items["none"],30:items["none"],"dropTable":[Drop_Table(items["Camp_Fire"],1),1],"timeLeft":0,"itemTimeLeft":{27:0,28:0},"tier":0,"hp":[100,100],"resistance":0.95}}


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
        return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],25:item[25],26:item[26],27:item[27],28:item[28]} 
      if item["name"] == "Wood_Chest" or item["name"] == "Reinforced_Wood_Chest":
        return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-315)//90)],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],25:item[25],26:item[26],27:item[27],28:item[28],29:item[29],30:item[30],31:item[31],32:item[32],33:item[33]} 
      if item["name"] == "Iron_Safe" or item["name"] == "Steel_Safe":
        return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"sprites":item["sprites"][int((Get_Line_Angle([0,0],[mP[0]-960,mP[1]-540])-315)//90)],"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"],25:item[25],26:item[26],27:item[27],28:item[28],29:item[29],30:item[30],31:item[31],32:item[32],33:item[33],34:item[34],35:item[35],36:item[36],37:item[37],38:item[38],39:item[39],40:item[40]} 

  if item["blockType"] == "active":
    return {"name":item["name"],"blockType":item["blockType"],"type":item["type"],"active":item["active"],"onSprite":item["onSprite"],"offSprite":item["offSprite"],25:item[25],26:item[26],27:item[27],28:item[28],29:item[29],30:item[30],"dropTable":item["dropTable"],"timeLeft":item["timeLeft"],"itemTimeLeft":{27:item["itemTimeLeft"][27],28:item["itemTimeLeft"][28]},"tier":item["tier"],"hp":[item["hp"][0],item["hp"][0]],"resistance":item["resistance"]}
