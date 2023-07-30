from variables import variables

def Get_Chunk(xPos,yPos,mapChunkX,chunkSize):
    chunkX = int(xPos//chunkSize) 
    chunkY = int(yPos//chunkSize)
    return chunkY*mapChunkX+chunkX

def Get_Square(xPos,yPos,chunkSize):
    x = int(xPos-(xPos//chunkSize)*chunkSize)
    y = int(yPos-(yPos//chunkSize)*chunkSize)
    return (chunkSize*(y+1))-(chunkSize-x)

def Get_Chunk_Clicked(mapChunkSizeX,chunkSize,posClickedX,posClickedY):
   x = ((posClickedX - 928)//64)+variables["player"]["position"][0]
   y = ((posClickedY - 508)//64)+variables["player"]["position"][1]
   return Get_Chunk(x,y,mapChunkSizeX,chunkSize)

def Get_Square_Clicked(chunkSize,posClickedX,posClickedY):
   x = ((posClickedX - 928)//64)+variables["player"]["position"][0]
   y = ((posClickedY - 508)//64)+variables["player"]["position"][1]
   return Get_Square(x,y,chunkSize)

def Get_Square_Cord(cordClickedX,cordClickedY):
  x = ((cordClickedX - 928)//64)+variables["player"]["position"][0]
  y = ((cordClickedY - 508)//64)+variables["player"]["position"][1]
  return [x,y]

def Get_Chunks_To_Draw(ChunkSizeX,ChunkSizeY,x,y,xBlock,yBlock):
    if (xBlock == 15 or xBlock == 16) and (yBlock >= 8 and yBlock <= 23): 
      return [[x,y]]
    elif (xBlock >= 0 and xBlock <= 14) and (yBlock >= 8 and yBlock <= 23): 
      if x - 1 >= 0:
        return [[x,y],[x-1,y]]
      else:
        return [[x,y]]
    elif (xBlock >= 17 and xBlock <= 31) and (yBlock >= 8 and yBlock <= 23): 
      if x + 1 <= ChunkSizeX-1:
        return [[x,y],[x+1,y]]
      else:
        return [[x,y]]   
    elif (xBlock == 15 or xBlock == 16) and (yBlock >= 0 and yBlock <= 7): 
      if y - 1 >= 0:
        return [[x,y],[x,y-1]]
      else:
        return [[x,y]]   
    elif (xBlock == 15 or xBlock == 16) and (yBlock >= 24 and yBlock <= 31): 
      if y + 1 <= ChunkSizeY:
        return [[x,y],[x,y+1]]
      else:
        return [[x,y]]     
    elif (xBlock >= 0 and xBlock <= 14) and (yBlock >= 0 and yBlock <= 7): 
      if x - 1 >= 0 and y - 1 >= 0:
        return [[x,y],[x-1,y-1],[x-1,y],[x,y-1]]
      elif x - 1 >= 0:
        return [[x,y],[x-1,y]]
      elif y - 1 >= 0:
        return [[x,y],[x,y-1]]
      else:
        return [[x,y]] 
    elif (xBlock >= 17 and xBlock <= 31) and (yBlock >= 0 and yBlock <= 7): 
      if x + 1 <= ChunkSizeX-1 and y - 1 >= 0:
        return [[x,y],[x+1,y-1],[x+1,y],[x,y-1]]
      elif x + 1 <= ChunkSizeX-1:
        return [[x,y],[x+1,y]]
      elif y - 1 >= 0:
        return [[x,y],[x,y-1]]
      else:
        return [[x,y]] 
    elif (xBlock >= 17 and xBlock <= 31) and (yBlock >= 24 and yBlock <= 31):
      if x + 1 <= ChunkSizeX-1 and y + 1 <= ChunkSizeY-1:
        return [[x,y],[x+1,y+1],[x+1,y],[x,y+1]]
      elif x + 1 <= ChunkSizeX-1:
        return [[x,y],[x+1,y]]
      elif y + 1 <= ChunkSizeY-1:
        return [[x,y],[x,y+1]]
      else:
        return [[x,y]] 
    elif (xBlock >= 0 and xBlock <= 14) and (yBlock >= 24 and yBlock <= 31):
      if x - 1 >= 0 and y + 1 <= ChunkSizeY-1:
        return [[x,y],[x-1,y+1],[x-1,y],[x,y+1]]
      elif x - 1 >= 0:
        return [[x,y],[x-1,y]]
      elif y + 1 <= ChunkSizeY-1:
        return [[x,y],[x,y+1]]
      else:
        return [[x,y]]
      
def Check_If_Block_Pix(map,mP):
    if map[Get_Chunk_Clicked(variables["mapChunkSize"][0],32,int(mP[0]),int(mP[1]))]["chunk"][Get_Square_Clicked(32,int(mP[0]),int(mP[1]))]["baseBlock"]["type"] == None:
      return False
    else:
      return True
    
def Check_If_Block_Cord(map,cords):
    if map[Get_Chunk(cords[0],cords[1],variables["mapChunkSize"][0],32)]["chunk"][Get_Square(cords[0],cords[1],32)]["baseBlock"]["type"] == None:
      return False
    else:
      return True