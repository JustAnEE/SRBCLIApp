from cli import CLI 



def main():
    
    CommandLine = CLI() 

    # Check if user has provided a .json config
    # object and read it in if found.  
    CommandLine.ScanForAndLoadJSONConfig()

    while(not CommandLine.IsDone()):
        CommandLine.ContinueReadingUserInput()


    return


if __name__ == "__main__":
    main() 
