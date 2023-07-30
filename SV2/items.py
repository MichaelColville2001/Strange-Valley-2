from stuff import LO

def Make_Base_info(name,type,stacks):
  return {"name":name,"type":type,"stacks":stacks,"invSprite":LO(f"invView/{name}"),"itemSprite":LO(f"itemSprite/{name}")}

items = {"none":{"baseInfo":{"name":None,"type":None,"stacks":False,"invSprite":None,"itemSprite":None},"speed":15},
         
        ##############################################################################################################################################################################

        "Camp_Fire":{"baseInfo":Make_Base_info("Camp_Fire","hand",False),"first":"block","second":"active","tier":1,"speed":0,"coolDown":0}, 



        "Fired_Clay_Pot":{"baseInfo":Make_Base_info("Fired_Clay_Pot","hand",False),"first":"block","second":"inActive","tier":1,"speed":0,"coolDown":0},   
        "Wood_Chest":{"baseInfo":Make_Base_info("Wood_Chest","hand",False),"first":"block","second":"inActive","tier":2,"speed":0,"coolDown":0},   
        "Reinforced_Wood_Chest":{"baseInfo":Make_Base_info("Reinforced_Wood_Chest","hand",False),"first":"block","second":"inActive","tier":3,"speed":0,"coolDown":0},   
        "Iron_Safe":{"baseInfo":Make_Base_info("Iron_Safe","hand",False),"first":"block","second":"inActive","tier":4,"speed":0,"coolDown":0},   
        "Steel_Safe":{"baseInfo":Make_Base_info("Steel_Safe","hand",False),"first":"block","second":"inActive","tier":5,"speed":0,"coolDown":0},   

        #"Clay_Brick_Wall":{"baseInfo":Make_Base_info("Clay_Brick_Wall","hand",False),"first":"block","second":"inActive","tier":1,"speed":0,"coolDown":0},  
        
        #"Clay_Brick_Window":{"baseInfo":Make_Base_info("Clay_Brick_Window","hand",False),"first":"block","second":"inActive","tier":1,"speed":0,"coolDown":0}, 

        #"Clay_Brick_Door":{"baseInfo":Make_Base_info("Clay_Brick_Door","hand",False),"first":"block","second":"inActive","tier":1,"speed":0,"coolDown":0}, 

        "Pry_Stick":{"baseInfo":Make_Base_info("Pry_Stick","hand",False),"first":"tool","second":"pick","tier":1,"damage":10,"durability":[100,100],"speed":20},
        "Stone_Axe":{"baseInfo":Make_Base_info("Stone_Axe","hand",False),"first":"tool","second":"axe","tier":1,"damage":10,"durability":[100,100],"speed":20},
        "Stone_Knife":{"baseInfo":Make_Base_info("Stone_Knife","hand",False),"first":"tool","second":"knife","tier":1,"durability":[1,1],"damage":10,"speed":0,"coolDown":1},

        #"Wood_Sheild":{"baseInfo":Make_Base_info("Wood_Sheild","hand",False)},
        
        #"Wood_Club":{"baseInfo":Make_Base_info("Wood_Club","hand",False)},
        #"Wood_Pike":{"baseInfo":Make_Base_info("Wood_Pike","hand",False)},

        #"Primitive_Wood_Bow":{"baseInfo":Make_Base_info("Primitive_Wood_Bow","hand",False)},
        #"Sling":{"baseInfo":Make_Base_info("Sling","hand",False)},

        ##########################################################################################################################################################################

        "Stone":{"baseInfo":Make_Base_info("Stone","inv",True),"stack":[1,8]},
        "Clay":{"baseInfo":Make_Base_info("Clay","inv",True),"stack":[1,8]},
        "Log":{"baseInfo":Make_Base_info("Log","inv",True),"stack":[1,8]},
        #"Stick":{"baseInfo":Make_Base_info("Stick","inv",True),"stack":[1,8]},
        #"Sap":{"baseInfo":Make_Base_info("Sap","inv",True),"stack":[1,8]},
        #"Thatch":{"baseInfo":Make_Base_info("Thatch","inv",True),"stack":[1,8]},
        #"Charcoal":{"baseInfo":Make_Base_info("Charcoal","inv",True),"stack":[1,8]},
        #"String":{"baseInfo":Make_Base_info("String","inv",True),"stack":[1,8]},
        #"Leather":{"baseInfo":Make_Base_info("Leather","inv",True),"stack":[1,8]},
        #"Leather_Strip":{"baseInfo":Make_Base_info("Leather_Strip","inv",True),"stack":[1,8]},
        #"Wolf_Pelt":{"baseInfo":Make_Base_info("Wolf_Pelt","inv",True),"stack":[1,8]},
        #"Wolf_Tooth":{"baseInfo":Make_Base_info("Wolf_Tooth","inv",True),"stack":[1,8]},
        #"Wood_Arrow":{"baseInfo":Make_Base_info("Wood_Arrow","inv",True),"stack":[1,8]},
        
        "Primitive_Wood_Axe_Handle":{"baseInfo":Make_Base_info("Primitive_Wood_Axe_Handle","inv",False)},
        #"Primitive_Unstrung_Bow":{"baseInfo":Make_Base_info("Primitive_Unstrung_Bow","inv",False)},
        #"Primitive_Wood_Sheild_Handle":{"baseInfo":Make_Base_info("Primitive_Wood_Sheild_Handle","inv",False)},
        #"Modern_Wood_Knife_Handle":{"baseInfo":Make_Base_info("Modern_Wood_Knife_Handle","inv",False)},
        #"Modern_Wood_Hammer_Handle":{"baseInfo":Make_Base_info("Modern_Wood_Hammer_Handle","inv",False)},
        #"Modern_Wood_Pick_Handle":{"baseInfo":Make_Base_info("Modern_Wood_Pick_Handle","inv","inv",False)},
        #"Modern_Wood_Axe_Handle":{"baseInfo":Make_Base_info("Modern_Wood_Axe_Handle","inv",False)},

        #"Fired_Clay_Brick":{"baseInfo":Make_Base_info("Fired_Clay_Brick","inv",True),"stack":[1,8]},
        #"Fired_Clay_Ingot_Mould":{"baseInfo":Make_Base_info("Fired_Clay_Ingot_Mould","inv",False)},
        #"Fired_Clay_Axe_Head_Mould":{"baseInfo":Make_Base_info("Fired_Clay_Axe_Head_Mould","inv",False)},
        #"Fired_Clay_Pick_Head_Mould":{"baseInfo":Make_Base_info("Fired_Clay_Pick_Head_Mould","inv",False)},
        #"Fired_Clay_Hammer_Head_Mould":{"baseInfo":Make_Base_info("Fired_Clay_Hammer_Head_Mould","inv",False)},
        #"Fired_Clay_Knife_Blade_Mould":{"baseInfo":Make_Base_info("Fired_Clay_Knife_Blade_Mould","inv",False)},
        
        #"Clay_Brick":{"baseInfo":Make_Base_info("Clay_Brick","inv",True),"stack":[1,8]},
        #"Clay_Pot":{"baseInfo":Make_Base_info("Clay_Pot","inv",False)},
        #"Clay_Ingot_Mould":{"baseInfo":Make_Base_info("Clay_Ingot_Mould","inv",False)},
        #"Clay_Axe_Head_Mould":{"baseInfo":Make_Base_info("Clay_Axe_Head_Mould","inv",False)},
        #"Clay_Pick_Head_Mould":{"baseInfo":Make_Base_info("Clay_Pick_Head_Mould","inv",False)},
        #"Clay_Hammer_Head_Mould":{"baseInfo":Make_Base_info("Clay_Hammer_Head_Mould","inv",False)},
        #"Clay_Knife_Blade_Mould":{"baseInfo":Make_Base_info("Clay_Knife_Blade_Mould","inv",False)},

        ###############################################################################################################################################################################


        }

def Convert_Item(item):
  type = item["baseInfo"]["type"]
  if type == None:
    return {"baseInfo":{"name":None,"type":None,"stacks":False,"invSprite":None,"itemSprite":None}}
  elif type == "inv":
    if item["baseInfo"]["stacks"]:
      return {"baseInfo":item["baseInfo"],"stack":item["stack"].copy()}
    elif not item["baseInfo"]["stacks"]:
      return {"baseInfo":item["baseInfo"]}
  elif type == "hand":
    if item["first"] == "tool":
      if item["second"] == "pick" or "axe":
        return {"baseInfo":item["baseInfo"],"first":item["first"],"second":item["second"],"tier":item["tier"],"damage":item["damage"],"durability":[item["durability"][0],item["durability"][1]],"speed":item["speed"]}
      if item["second"] == "knife":
        return {"baseInfo":item["baseInfo"],"first":item["first"],"second":item["second"],"tier":item["tier"],"damage":item["damage"],"durability":[item["durability"][0],item["durability"][1]],"speed":item["speed"],"coolDown":item["coolDown"]}
    elif item["first"] == "block":
      if item["second"] == "active" or "inActive":
        return {"baseInfo":item["baseInfo"],"first":item["first"],"second":item["second"],"tier":item["tier"],"speed":item["speed"],"coolDown":item["coolDown"]}
  elif type == "helm":
    return {"baseInfo":item["baseInfo"]}
  