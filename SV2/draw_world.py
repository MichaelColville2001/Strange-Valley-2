from stuff import Get_Sprite,LO
from variables import variables
from get_cs import Get_Chunk,Get_Chunks_To_Draw
from item_stuff import Pick_up_item
from init import Win,HEIGHT,WIDTH

def Draw_Chunk(chunk):
    for block in range(1024):
       if chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0] >= -64 and chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0] <= WIDTH and chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1] >= -64 and chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1] <= HEIGHT:
          Win.blit(Get_Sprite(chunk["chunk"][block]["floorBlock"]["sprites"],(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0],chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1])))
          if chunk["chunk"][block]["baseBlock"]["blockType"] == "active":
            if chunk["chunk"][block]["baseBlock"]["active"]:
              Win.blit(Get_Sprite(chunk["chunk"][block]["baseBlock"]["onSprite"],(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0],chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1])))
              num = int(chunk["chunk"][block]["baseBlock"]["hp"][0]//(chunk["chunk"][block]["baseBlock"]["hp"][1]//5))
              if not num == 5:
                Win.blit(Get_Sprite(LO(f"blockBreaking/blockBreak{num}"),(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0],chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1])))
            if not chunk["chunk"][block]["baseBlock"]["active"]:
              Win.blit(Get_Sprite(chunk["chunk"][block]["baseBlock"]["offSprite"],(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0],chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1])))
              num = int(chunk["chunk"][block]["baseBlock"]["hp"][0]//(chunk["chunk"][block]["baseBlock"]["hp"][1]//5))
              if not num == 5:
                Win.blit(Get_Sprite(LO(f"blockBreaking/blockBreak{num}"),(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0],chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1])))
          elif not chunk["chunk"][block]["baseBlock"]["sprites"] == None:
            Win.blit(Get_Sprite(chunk["chunk"][block]["baseBlock"]["sprites"],(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0],chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1])))
            num = int(chunk["chunk"][block]["baseBlock"]["hp"][0]//(chunk["chunk"][block]["baseBlock"]["hp"][1]//5))
            if not num == 5:
              Win.blit(Get_Sprite(LO(f"blockBreaking/blockBreak{num}"),(0,0,0),64),((chunk["chunk"][block]["position"][0]*64-variables["relativePerspective"][0],chunk["chunk"][block]["position"][1]*64-variables["relativePerspective"][1])))

def Draw_Screen(map):
    chunkSpot = variables["player"]["position"][0]-(((variables["player"]["position"][0])//32)*32),variables["player"]["position"][1]-(((variables["player"]["position"][1])//32)*32)
    inChunk = map[Get_Chunk(variables["player"]["position"][0],variables["player"]["position"][1],variables["mapChunkSize"][0],32)]["chunkPosition"]
    chunkCords = Get_Chunks_To_Draw(variables["mapChunkSize"][0],variables["mapChunkSize"][1],inChunk[0],inChunk[1],chunkSpot[0],chunkSpot[1])
    for chunk in range(len(chunkCords)):
      Draw_Chunk(map[Get_Chunk((((chunkCords[chunk][0]+1)*32)-1),(((chunkCords[chunk][1]+1)*32)-1),variables["mapChunkSize"][0],32)])


def Draw_Item_Chunk(chunk):
    if len(chunk["chunk"]) > 0:
      for item in range(len(chunk["chunk"])):
        if chunk["chunk"][item]["position"][0]-variables["relativePerspective"][0] >= -32 and chunk["chunk"][item]["position"][0]-variables["relativePerspective"][0] <= WIDTH and chunk["chunk"][item]["position"][1]-variables["relativePerspective"][1] >= -32 and chunk["chunk"][item]["position"][1]-variables["relativePerspective"][1] <= HEIGHT:
          Win.blit(Get_Sprite(chunk["chunk"][item]["item"]["baseInfo"]["itemSprite"],(0,0,0),64),((chunk["chunk"][item]["position"][0]-variables["relativePerspective"][0],chunk["chunk"][item]["position"][1]-variables["relativePerspective"][1])))

def Draw_Screen_Items(map):
    chunkSpot = variables["player"]["position"][0]-(((variables["player"]["position"][0])//32)*32),variables["player"]["position"][1]-(((variables["player"]["position"][1])//32)*32)
    inChunk = map[Get_Chunk(variables["player"]["position"][0],variables["player"]["position"][1],variables["mapChunkSize"][0],32)]["chunkPosition"]
    chunkCords = Get_Chunks_To_Draw(variables["mapChunkSize"][0],variables["mapChunkSize"][1],inChunk[0],inChunk[1],chunkSpot[0],chunkSpot[1])
    for chunk in range(len(chunkCords)):
      Draw_Item_Chunk(map[Get_Chunk((((chunkCords[chunk][0]+1)*32)-1),(((chunkCords[chunk][1]+1)*32)-1),variables["mapChunkSize"][0],32)])
      Pick_up_item(map[Get_Chunk((((chunkCords[chunk][0]+1)*32)-1),(((chunkCords[chunk][1]+1)*32)-1),variables["mapChunkSize"][0],32)])