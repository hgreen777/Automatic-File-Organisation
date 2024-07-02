# Imports
import os       # OS (checking directories)
import shutil   # File Operation
import re       # Regex
import csv      # CSV operations 

# TODO : (Potential use binary tree to make searching for routes more efficient)

# Must swith \ to / or breaks
# Original Path to check where for new files
# Input directory for sorting files
startPATH = r"H:\hjgre\Pictures\Saved Pictures"

routes = []

# Create Dictionary of available routes
def readCSV():
    # Read all the codes into a dictionary.
    with open("./Routes.csv", mode='r') as file:
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
def findDestination(codes, routes, filename):
    # Loop over codes and check if in destination

    # Base Case
    for route in routes:
        if route['code'] == "XX":
            destination = route['path']
            break

    # Find if there is a valid base path
    for route in routes:
        if route['code'] == codes[0]:
            destination = route['path']

            # Check for further extentions
            # TODO : Make more efficient (seperate CSV) - this will ensure it is a valid extension?
            for index, code in enumerate(codes):
                if index == 0 or code == "rm":
                    continue
                for route in routes:
                    if route['code'] == code:
                        destination += route['path']

            break

    # If there is, check any further extentions
    

    if "rm" in codes:
        filename = cleanName(filename)
        return destination, filename, True
    
    return destination,filename, False

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

     
# TODO : Put all functions togethor for actual inplementation, & testing, renaming files and moving files need to be tested, update startPATH, remove testStr with acc things
# TODO : ensure that does not break if destination does not exist or file name problem etc.
# TODO : Documentation

def main():

    readCSV()               # Create Dictionary
    testStr = "test_.file._SC-PH-rm.txt"
    codes = obtainCodes(testStr)    # Obtain the codes from the given file
    #TODO Change returns name
    returns = findDestination(codes, routes, testStr)

    #So code dont run
    if False:
    #if returns[2] == True:
        os.rename((startPATH + "/" + testStr),)
    print(returns[0])
    print(returns[1])

main()
