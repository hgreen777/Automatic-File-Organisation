# Imports
import os       # OS (checking directories)
import shutil   # File Operation
import re       # Regex
import csv      # CSV operations 
import threading
import time

# TODO : (Potential use binary tree to make searching for routes more efficient)

# Must swith \ to / or breaks
# Original Path to check where for new files
# Input directory for sorting files
startPATH = r"H:\hjgre\Downloads2\DropSort"

routes = []

# Create Dictionary of available routes
def readCSV():
    # Read all the codes into a dictionary.
    with open("./Routes.csv", mode='r') as file:
        reader = csv.DictReader(file)

        for row in reader:
            routes.append(row)

def detectChange(path):
    allFiles = os.listdir(path) # Gets all files in the path in a list

    # Clean list
    if "Overflow" in allFiles:
        allFiles.remove("Overflow")
    if "Games" in allFiles:
        allFiles.remove("Games")
    
    return allFiles


def moveFile(file, newPath):
    oldPath = startPATH + "/" + file
    newPath = newPath + "/" + file

    shutil.move(oldPath, newPath)

    return 

# Route the file to correct destination (call moveFile based of code (search in dictionary for path)) (call clean file name if needed)
# Obtains code abreviations from filename from file name
def obtainCodes(fileName):
    # Remove FileType 
    mask = r"^(.*)(?=\.[^.]*$)"
    regex_name = re.findall(mask, fileName)
    # If it is a directory will not have a file type so nothing will be picked up in mask.
    if len(regex_name) != 0:
        fileName = regex_name[0]


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
    
    # For handling directorys
    mask = r"^(.*)(?=\.[^.]*$)"
    regex_name = re.findall(mask, fileName)
    # If it is a directory will not have a file type so nothing will be picked up in mask.
    if len(regex_name) == 0:
        mask = r"(_[^_]+)$"
        reg = re.findall(mask, fileName)
        fileName = fileName.replace(reg[0], "")
        return fileName
    
    return fileName

# TODO : Creating new locations from CLI input

# TODO : Manually Run Command (from CLI) / 

# TODO : Automatic Running / 
     
# TODO : Documentation

# Runs the process
def main():

    readCSV()

    files = detectChange(startPATH)

    for file in files:
        codes = obtainCodes(file)
        returns = findDestination(codes, routes, file)
        destination = returns[0]; filename = returns[1]; isNameChange = returns[2]

        # Chnage Name, Move file to new location
        moveFile(file,destination)

        if isNameChange:
            try:
                os.rename((destination + "/" + file), (destination+ "/" + filename))
            except Exception as e:
                print(f"File name has not been cleaned but may still have been relocated: Error Msg: {e}")

    
    print("Files moved Successfully ")

stop_thread = False

def automaticRun():
    global stop_thread
    while not stop_thread:
        main()
        time.sleep(600) # Wait 10mins

def startAutomatic():
    global stop_thread, auto
    stop_thread = False
    auto = threading.Thread(target=automaticRun)
    auto.start()

def stopAutomatic():
    global stop_thread
    stop_thread = True
    auto.join()


def userInput():
    startupInput = input("Auto-File-Organizer : Command: (h for help): ") 

    if startupInput == "h":
        print("Commands: h = help menu giving available commands \n a = start automatic processing \n m = begin a manual process (stops automatic) \n c = create new route/extension \n q = quit automatic")
    elif startupInput == "a":
        startAutomatic()
    elif startupInput == "m":
        main()
        stopAutomatic()
    elif startupInput == "q":
        stopAutomatic()
        print("Quitting automatic process.")
        return
    
    userInput()



userInput()








