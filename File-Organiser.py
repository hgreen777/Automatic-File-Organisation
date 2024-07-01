import os
import shutil

# Must swith \ to / or breaks
# Original Path to check where for new files
# Input directory for sorting files
startPATH = r"H:\hjgre\Pictures\Saved Pictures"

print(os.listdir(startPATH))


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

# TODO : Clean File Name 

# TODO : Creating new locations from CLI input

# TODO : Manually Run Command (from CLI)

# TODO : Automatic Running

# TODO : Creating Graphic
     


files_to_sort = dectectChange(startPATH)

print(files_to_sort)
