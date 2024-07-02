# Imports
import os       # OS (checking directories)
import shutil   # File Operation
import re       # Regex
import csv      # CSV operations 

# Must swith \ to / or breaks
# Original Path to check where for new files
# Input directory for sorting files
startPATH = r"H:\hjgre\Pictures\Saved Pictures"

routes = []

# Create Dictionary of available routes
def readCSV():
    # Locate path to the csv file 
    script_dir = os.path.dirname(os.path.realpath(__file__))
    path_csv = os.path.join(script_dir, "Routes.csv")

    # Read all the codes into a dictionary.
    with open(path_csv, mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            routes.append(row)


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

# Find destination based off codes (return destination (call clean name if needed))


# Clean File Name
def cleanName(fileName):
    mask = r"(_[^_]+)(?=\.[^.]*$)"

    match = re.search(mask, fileName)

    if match:
        fileName = fileName.replace(match[0], "")
        return fileName
    
    return fileName



# TODO : Creating new locations from CLI input

# TODO : Manually Run Command (from CLI)

# TODO : Automatic Running

# TODO : Creating Graphic
     


testStr = "test_.file._CD-FD-rm.txt"
print(routes)
readCSV()
print(routes)
