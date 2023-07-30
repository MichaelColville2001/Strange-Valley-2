from blocks import Convert_Blocks,baseBlocks,floorBlocks
from random import randint
from variables import variables

def Make_Chunks(ChunkSizeX,ChunkSizeY):
    map = []
    for y in range(ChunkSizeY):
      for x in range(ChunkSizeX):
        chunk = []
        for yBlock in range(32):
          for xBlock in range(32):
            floor = Convert_Blocks(floorBlocks["Grass"])
            base = Convert_Blocks(baseBlocks["none"])
            if randint(0,20) == 1:
              int = randint(0,3)
              if int == 0:
                base = Convert_Blocks(baseBlocks["Rock"])
              if int == 1:
                base = Convert_Blocks(baseBlocks["Log"])
              if int == 2:
                base = Convert_Blocks(baseBlocks["Rock_Pile"])
              if int == 3:
                base = Convert_Blocks(baseBlocks["Bush"])
            if base  == baseBlocks["none"]:
              if randint(0,100) == 1:
                variables["player"]["position"][0] = xBlock
                variables["player"]["position"][1] = yBlock
            chunk.append({"position":[xBlock+(x*32),yBlock+(y*32)],"floorBlock":floor,"baseBlock":base})
        map.append({"chunkPosition":[x,y],"chunk":chunk})
    return map

def Make_Basic_Chunks(ChunkSizeX,ChunkSizeY):
    map = []
    for y in range(ChunkSizeY):
      for x in range(ChunkSizeX):
        chunk = []
        map.append({"chunkPosition":[x,y],"chunk":chunk})
    return map