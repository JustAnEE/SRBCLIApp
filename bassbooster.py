from dictionaries import UserInputValidKeys
import numpy as np 
from scipy.signal import lfilter 
from scipy.signal import fftconvolve 
from scipy.io import wavfile 
import warnings
import os 
from compressor import Compressor

# We're using a cooked .wav type, ignore the non-data chunk
# warning 
warnings.filterwarnings("ignore", lineno=46)
warnings.filterwarnings("ignore", lineno=51)
warnings.filterwarnings("ignore", lineno=176)
class BassBooster:

   def __init__(self):

      # Fields 
      self.__MySampleRate = 0 
      self.__MyNyquist = 0 
      self.__MyGain = 0 
      self.__MyFrequencyWarpFactor = 0
      self.__MyCuttoffHz = 0 
      self.__MyNormalizedCuttoff = 0
      self.__MyData = None 
      self.__MyImpulseResponse = None 
      self.__MyPercentSlowed = 0 
      self.__MyChannelLength = 0 
      self.__MyLocation = "" 
      self.__MyWavFileLocation = ""
      self.__MyThroughLineScale = 0.85
      self.__MyReverbScale = 0.15
      # Objects 
      self.__MyCompressor = Compressor()
      return 

   
   #!TODO: Create a dictionary of keys shared by multiple objects 
   # which each object can loop over to replace 
   # this disgusting boof 
   def InitFromJSONConfig(self, JSONConfig: dict)->None:

      if (JSONConfig.get("WavFileLoc") is not None):
         self.__MyWavFileLocation = JSONConfig["WavFileLoc"]
         self.__MySampleRate, self.__MyData = wavfile.read(self.__MyWavFileLocation)
         # The output will be in the same directory as the input by default 
         self.__MyLocation = os.path.dirname(JSONConfig['WavFileLoc'])
      
      if (JSONConfig.get("CustomImpulseResponseLoc") is not None):
         ImpulseRate, self.__MyImpulseResponse = wavfile.read(JSONConfig["CustomImpulseResponseLoc"]) 

      if (JSONConfig.get("Gain") is not None):
         self.__MyGain = JSONConfig["Gain"]

      if (JSONConfig.get("LowShelfCutoffHz") is not None):
         self.__MyCuttoffHz = JSONConfig["LowShelfCutoffHz"]
      
      if (JSONConfig.get("PercentSlowed") is not None):
         self.__MyPercentSlowed = JSONConfig["PercentSlowed"]/100
   

      # After loading from user facing parameters, init parameters the 
      # user does not need to know 
      self.__InitParameters()

      return 
   
   def __InitParameters(self)->None:
      
      self.__MyNyquist = (1/2)*self.__MySampleRate
      self.__MyNormalizedCuttoff = np.pi*(self.__MyCuttoffHz/self.__MyNyquist)
      self.__MyFrequencyWarpFactor = np.tan(self.__MyNormalizedCuttoff/2)
      self.__MyChannelLength = len(self.__MyData)
      
      # Create a fake stereo file if the file is mono  
      if(self.__IsMono()):
         self.__CreateFakeStereo()
      
      return 

   def __IsMono(self)->bool:
      return np.size(np.shape(self.__MyData)) == 1
   
   def __CreateFakeStereo(self)->None:
      
      LeftChannel = self.__MyData
      RightChannel = self.__MyData

      StereoData = np.zeros((self.__MyChannelLength,2), dtype=np.float32)
      StereoData[:, 0] = LeftChannel
      StereoData[:, 1] = RightChannel
      
      self.__MyData = StereoData
      return

   def __ApplyReverb(self):
      
      self.__MyData[:, 0] = fftconvolve(self.__GetAudioChannel('left'), self.__GetImpulseChannel('left'))[0:self.__MyChannelLength]

      self.__MyData[:, 1] = fftconvolve(self.__GetAudioChannel('right'), self.__GetImpulseChannel('right'))[0:self.__MyChannelLength]
      return 

   def __GetLowShelfParams(self):
      
      b_0 = 1 + np.sqrt(2*self.__MyGain)*self.__MyFrequencyWarpFactor + self.__MyGain*(self.__MyFrequencyWarpFactor)**2
      b_1 = -2 + 2*self.__MyGain*self.__MyFrequencyWarpFactor**2
      b_2 = 2 - b_0 + 2*self.__MyGain*self.__MyFrequencyWarpFactor**2

      a_0 = 1 + np.sqrt(2) * self.__MyFrequencyWarpFactor + self.__MyFrequencyWarpFactor**2
      a_1 = -2 + 2 *self.__MyFrequencyWarpFactor **2 
      a_2 = 2 - a_0 + 2*self.__MyFrequencyWarpFactor**2

      bVector = np.array([b_0, b_1, b_2])
      aVector = np.array([a_0, a_1, a_2])

      return bVector, aVector 


   def __ApplyLowShelf(self)->None:

      b, a = self.__GetLowShelfParams()

      LowShelvedData = lfilter(b, a, self.__MyData, axis = 0)

      # Ensure the resulting type is float 32 
      LowShelvedData = np.asarray(LowShelvedData, dtype=np.float32)
      
      self.__MyData = LowShelvedData
      return 

   def __GetAudioChannel(self, channel='left')->np.ndarray:
      
      if (channel == 'left'):
         return self.__MyData[:, 0]
      
      else:
         return self.__MyData[:, 1]
      

   def __GetImpulseChannel(self, channel='left'):

      if (channel == 'left'):
         return self.__MyImpulseResponse[:, 0]

      else:
         return self.__MyImpulseResponse[:, 1]
 
   def SlowReverbAndBoost(self)->None:
      
      # Apply the shelving filter 
      self.__ApplyLowShelf()
     
      # Deep copy original audio through line 
      OriginalAudio = np.array(self.__MyData)

      # Apply the impulse response for the reverberation 
      self.__ApplyReverb()


      # Apply the processed data to the original audio to keep 
      # some of the original sound
      self.__MyData = self.__MyReverbScale*self.__MyData + self.__MyThroughLineScale*OriginalAudio
      
      # Write the audio slowed 
      OutLocation = self.__MyLocation + "\\Output.wav"      
      SlowedRate = int((1-self.__MyPercentSlowed)*self.__MySampleRate)
    
      wavfile.write(OutLocation, SlowedRate, self.__MyData)

      #!TODO: Most boof of them all :) 
      # REREAD THE FILE KEKW
      # To Fix: We need a separate copy of the data which exists untouched
      # what's happening is the processed data is becoming the new "input" data 
      # cascading effects of processing 
      self.__MySampleRate, self.__MyData = wavfile.read(self.__MyWavFileLocation)

      return 


   def UpdateGain(self, Gain)->None:
      self.__MyGain = Gain 
      return 

   def UpdatePercentSlowed(self, PercentSlowed)->None:
      self.__MyPercentSlowed = PercentSlowed/100
      return 

   def UpdateScales(self, ReverbScale_, ThroughScale_) ->None:
      self.__MyReverbScale = ReverbScale_
      self.__MyThroughLineScale = ThroughScale_
      return 

   def CompressToMP3(self)->None:

      self.__MyCompressor.SetLocation(self.__MyLocation + "\\Output.wav")
      self.__MyCompressor.ExportWAVToMP3()
      return 




