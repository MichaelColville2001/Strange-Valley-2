from stuff import LO
from items import items,Convert_Item


variables = {
"viewCord":[[1,0],[1,-1],[0,-1],[-1,-1],[-1,0],[-1,1],[0,1],[1,1]],

"assembelyNames":["Stone_Knife","Stone_Axe","Camp_Fire","Clay_Pot"],

"carvingNames":["Pry_Stick","Primitive_Wood_Axe_Handle"],

###

"mapChunkSize":[25,25], #small 25x25 medium 50x50 large 100x100

"running": True,
 
###

"relativePerspective":[0,0],

"mouseState":"",

"leftRightMouseButton":[False,False,False],

"invOn":False,

"shift":False,
"w":False,
"a":False,
"s":False,
"d":False,

###

"player":{"position": [10,10],
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

          0: Convert_Item(items["Fired_Clay_Pot"]),1: Convert_Item(items["Fired_Clay_Pot"]),2: Convert_Item(items["Camp_Fire"]),3: items["none"],
          4: items["none"],5: items["none"],6: items["none"],7: items["none"],
          8: items["none"],9: items["none"],10: items["none"],11: items["none"],
          12: items["none"],13: items["none"],14: items["none"],15: items["none"], #inv
          16: items["none"], #LH
          17: items["none"], #RH
          18: items["none"], #helm
          19: items["none"], #chest
          20: items["none"], #legs
          21: items["none"], #boots
          22: items["none"], #gloves
          23: items["none"], #craftingTool
          24: items["none"]} #craftingTool

}