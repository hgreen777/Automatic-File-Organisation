# Imports
import os       #OS (checking directories)
import shutil   # File Operation
import re       #Regex

# Must swith \ to / or breaks
# Original Path to check where for new files
# Input directory for sorting files
startPATH = r"H:\hjgre\Pictures\Saved Pictures"


def dectectChange(path):
    allFiles = os.listdir(path) # Gets all files in the path in a list

    # Clean list
    if "Overflow" in allFiles:
        allFiles.remove("Overflow")
    
    return allFiles

# TODO : Test
def moveFile(file, newPath):
    oldPath = startPATH + "/" + file

    shutil.move(oldPath, newPath)

# TODO : Create Dictionary based of available routes

# TODO : Route the file to correct destination (call moveFile based of code (search in dictionary for path)) (call clean file name if needed)


    # Obtains code abreviations from filename from file name
def obtainCodes(fileName):
    # Remove FileType 
    mask = r"^(.*)(?=\.[^.]*$)"
    fileName = re.findall(mask, fileName)
    fileName = fileName[0] # Select first item in list (findall returns list)

    # Obtain Code
    mask = r"\_[^_]*$"
    fileName = re.findall(mask, fileName)   
    fileName = fileName[0] # Select first item in list (findall returns list)

    fileName = fileName[1:]

    # Split codes into seperate code in a list
    mask = r"[^-]+"

    codes = re.findall(mask, fileName)
    return codes



# TODO : Clean File Name 

# TODO : Creating new locations from CLI input

# TODO : Manually Run Command (from CLI)

# TODO : Automatic Running

# TODO : Creating Graphic
     


testStr = "test .File._CD-FD-rm.txt"
print(obtainCodes(testStr))

