
# Configuration strings 
JSONFoundString = "Found Configuration File..."
ConfigurationString = "Found the following valid configuration keys... \n{}"
ProcessingDoneString = "Processing the input .wav file is complete... \n"
CompressionDoneString = "Compressor has compressed output to .mp3... \n"
UnknownCommandString = "Command not recognized. See -h or help for help...\n"

# General help string 
HelpString = \
"This is a simple command line bassboosting, slowing and reverbing app. \n"\
+"---------------------------------- Config Help --------------------------------------\n"\
+"The app on start up scans the directory the CLI is in for a config.json object which \n"\
+"will be used to initialize the program. The program is looking for a config.json which \n"\
+"has the following keys: \n"\
+"WavFileLoc: An absolute path to the .wav file we want to process.\n"\
+"Gain: A number used to linearly scale the bass frequencies boosted by the shelving filter.\n"\
+"LowShelfCutoffHz: The frequency range to boost from (0, LowShelfCutoffHz) Hz\n"\
+"PercentSlowed: How much to slow the track by. \n"\
+"Default: \n"\
+"{ \n"\
+"   \"WavFileLoc\": \"This\\Is\\My\\Absolute\\Filepath\\stuff.wav\", \n"\
+"   \"Gain\": 3, \n"\
+"   \"LowShelfCutoffHz\": 120, \n"\
+    "\"PercentSlowed\": 10 \n"\
+"}\n"\
+"----------------------------------- Other Help ---------------------------------------\n"\
+"Parameters can be changed and set without a configuration file \n"\
+"updategain x -- will update the gain to x \n"\
+"updatepercentslowed x -- will update the percent slowed to x \n"\
+"eq x y -- will set the through line scale to x, and will set the reverb scale to y \n"\
+"    (default x = 0.5, y=0.5) \n"\
+"eq x% y% so entering the scales as a percentage is supported: eq 45 55. \n"\
+"After the configuration is set, either through .json configuration or through commands \n"\
+"the program can start by running \"runfromconfig\". The program will print out a statement\n"\
+"when the processing has completed. If the user wishes to convert the output to mp3, run \n"\
+"compresstomp3 -- compress output .wav to mp3 format (requires ffmpeg and pydub)\n"\
+"The command line will wait for further instructions, after listening to the audio \n"\
+"if the user wants to change a parameter, they can enter the command to change it and \n"\
+"then execute runfromconfig again. \n"


class StringPrinter:
    def __init__(self):

        self.__MyStringDict = {
            "JSONFOUND": JSONFoundString,
            "CONFIGURATION": ConfigurationString,
            "PROCESSINGDONE" : ProcessingDoneString,
            "COMPRESSIONDONE": CompressionDoneString,
            "UNRECOGNIZED" : UnknownCommandString,
            "HELP" : HelpString 
        }
        return 

    #!TODO: TURBO BOOF LMAO 
    def PrintString(self, key: str, dictionary: dict = None)->None:
        
        if(key == "CONFIGURATION" and (dictionary is not None)):
            
            OutStr = ""
            FrmtStr = "   {}: {}\n"
            for ConfigKey, ConfigVal in zip(dictionary.keys(), dictionary.values()):
                OutStr = OutStr + FrmtStr.format(ConfigKey,ConfigVal)
            print(self.__MyStringDict[key].format(OutStr))

        else:
            print(self.__MyStringDict[key])

        return 
