import pydub 
import os 

class Compressor:
   def __init__(self):

      self.__MyFileLocation = ""
      self.__MyOutputLocation = "" 
      return 
   
   
   def SetLocation(self, Loc: str)->None:
      
      self.__MyFileLocation = Loc
      # Set the output location to the same directory 
      # by default 
      Directory = os.path.dirname(self.__MyFileLocation)
      self.__MyOutputLocation = Directory + "\\outputcompressed.mp3"
      return 

   def ExportWAVToMP3(self)->None:
      
      TempFile = pydub.AudioSegment.from_wav(self.__MyFileLocation)
      #Temp = TempFile.compress_dynamic_range(threshold=-12.0, ratio=30.0, attack=10.0, release=200.0)
      TempFile.normalize() 
      TempFile.export(self.__MyOutputLocation, bitrate='192k', format='mp3')
      return 
