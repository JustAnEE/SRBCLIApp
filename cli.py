from validator import Validator
from filestrings import StringPrinter 
from bassbooster import BassBooster

import os 
import json 

class CLI:

    def __init__(self):

        # ---- Fields ----  
        self.__MyExitReceived = False 
        self.__MyAllowedToRun = False 
        self.__MyExitDict = {
            "quit" : 0, 
            "exit" : 1,
            "nuke" :2 
        }
        self.__MyCommandsDict = {
            "runfromconfig" : 0,
            "compressmp3" : 1, 
            "updategain" : 2,
            "updatepercentslowed" : 3,
            "compresstomp3" : 4,
            "eq" : 5,
            "-h" : 6,
            "help" : 7
        }
        self.__MyJSONConfig = None

        # ---- Objects ----
        self.__MyValidator = Validator()
        self.__MyPrinter = StringPrinter()
        self.__MyDSP = BassBooster() 

        return 

    def IsDone(self)->bool:
        return self.__MyExitReceived

    
    #!TODO: De-spaghettify
    def __ParseCommands(self, Commands: str)->None:
       
        RecognizedCommand = False 

        for key in self.__MyExitDict:
            if key in Commands:
                self.__MyExitReceived = True 
                return 
        
        
        for key in self.__MyCommandsDict:
            if (key in Commands):
                if (key == "runfromconfig"):
                    self.__MyAllowedToRun = True
                    RecognizedCommand = True 

                if ("updategain" in Commands):
                    Gain = float(Commands.split()[1])
                    self.__MyDSP.UpdateGain(Gain)
                    RecognizedCommand = True 

                if ("updatepercentslowed" in Commands):
                    PercentSlowed = int(Commands.split()[1])
                    self.__MyDSP.UpdatePercentSlowed(PercentSlowed)
                    RecognizedCommand = True 

                if ("compresstomp3" in Commands):
                    self.__MyDSP.CompressToMP3()
                    self.__MyPrinter.PrintString("COMPRESSIONDONE")
                    RecognizedCommand = True 

                if ("eq" in Commands):
                    Through = float(Commands.split()[1])
                    Reverb = float(Commands.split()[2])
                    if(Through > 1):
                       Through = Through / 100
                    if (Reverb > 1):
                       Reverb = Reverb / 100 

                    self.__MyDSP.UpdateScales(Reverb, Through)
                    RecognizedCommand = True 

                if ( ("-h" in Commands) or ("help") in Commands):
                    self.__MyPrinter.PrintString("HELP")
                    RecognizedCommand = True 

        # If we made it here, the user has entered a bad command 
        if(not RecognizedCommand):
            self.__MyPrinter.PrintString("UNRECOGNIZED")

        return 

    
    def ScanForAndLoadJSONConfig(self)->None:

        CurrentDir = os.path.dirname(__file__)
        FilesInDir = os.listdir(CurrentDir)
        EOF = -1 
        
        for File in FilesInDir:
            if ".json" in File:
                JSONLocation = CurrentDir + "\\" + File 
                JSONFileObj = open(JSONLocation)
                self.__MyJSONConfig = json.loads(JSONFileObj.read(EOF))
                self.__MyPrinter.PrintString("JSONFOUND")
                self.__MyPrinter.PrintString("CONFIGURATION", self.__MyJSONConfig)

                # Attempt to load the configuration into the DSP 
                self.__MyDSP.InitFromJSONConfig(self.__MyJSONConfig)
                JSONFileObj.close() 

        return 

    def ContinueReadingUserInput(self)->None:
        
        Commands = input() 
        if(self.__MyValidator.IsCommandValid(Commands)):
            self.__ParseCommands(Commands.lower())

            if(self.__MyAllowedToRun):
                self.__MyDSP.SlowReverbAndBoost()
                self.__MyPrinter.PrintString("PROCESSINGDONE")
                # Reset this after running 
                self.__MyAllowedToRun = False 
            

        return 
        



