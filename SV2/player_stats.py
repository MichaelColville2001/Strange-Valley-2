from variables import variables

def Change_Player_Stats():
    if variables["player"]["stam"][0] < variables["player"]["stam"][1]:
       variables["player"]["stam"][0] += 1
    if variables["player"]["hp"][0] < variables["player"]["hp"][1]:
       variables["player"]["hp"][0] += .1
    if variables["player"]["mana"][0] < variables["player"]["mana"][1]:
       variables["player"]["mana"][0] += .5