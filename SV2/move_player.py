from variables import variables
from get_cs import Check_If_Block_Cord
from stuff import If_Both_False

def Move_Line(map,speed,xy,x,y):
  if not Check_If_Block_Cord(map,[variables["player"]["position"][0]+x,variables["player"]["position"][1]+y]):
    variables["player"]["position"][xy] += y+x
    variables["player"]["stam"][0] -= speed

def Move_Diagonal(map,speed,x,y):
  if not Check_If_Block_Cord(map,[variables["player"]["position"][0]+x,variables["player"]["position"][1]+y]) and If_Both_False(Check_If_Block_Cord(map,[variables["player"]["position"][0],variables["player"]["position"][1]+y]),Check_If_Block_Cord(map,[variables["player"]["position"][0]+x,variables["player"]["position"][1]])):
        variables["player"]["position"][0] += x
        variables["player"]["position"][1] += y
        variables["player"]["stam"][0] -= speed

def Move_Player(map,speed):
    if variables["w"] and variables["a"] and variables["player"]["position"][1] > 0 and variables["player"]["position"][0] > 0 and variables["player"]["stam"][0] > speed:
      Move_Diagonal(map,speed,-1,-1)
    elif variables["w"] and variables["d"] and variables["player"]["position"][1] > 0 and variables["player"]["position"][0] < variables["mapChunkSize"][0]*32-1 and variables["player"]["stam"][0] > speed:
      Move_Diagonal(map,speed,1,-1)
    elif variables["s"] and variables["a"] and variables["player"]["position"][1] < variables["mapChunkSize"][1]*32-1 and variables["player"]["position"][0] > 0 and variables["player"]["stam"][0] > speed:
      Move_Diagonal(map,speed,-1,1)
    elif variables["s"] and variables["d"] and variables["player"]["position"][0] < variables["mapChunkSize"][0]*32-1 and variables["player"]["position"][1] < variables["mapChunkSize"][0]*32-1  and variables["player"]["stam"][0] > speed: 
      Move_Diagonal(map,speed,1,1)
    elif variables["w"] and variables["player"]["position"][1] > 0 and variables["player"]["stam"][0] > speed:
      Move_Line(map,speed,1,0,-1)
    elif variables["a"] and variables["player"]["position"][0] > 0 and variables["player"]["stam"][0] > speed:
      Move_Line(map,speed,0,-1,0)
    elif variables["s"] and variables["player"]["position"][1] < variables["mapChunkSize"][1]*32-1 and variables["player"]["stam"][0] > speed:
      Move_Line(map,speed,1,0,1)
    elif variables["d"] and variables["player"]["position"][0] < variables["mapChunkSize"][0]*32-1 and variables["player"]["stam"][0] > speed: 
      Move_Line(map,speed,0,1,0)