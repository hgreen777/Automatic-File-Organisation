import os
import shutil

# Must swith \ to / or breaks
path = r"H:\hjgre\Pictures\Saved Pictures"

print(os.listdir(path))


def dectectChange(path):
    allFiles = os.listdir(path) # Gets all files in the path in a list

    # Clean list
    if "Overflow" in allFiles:
        allFiles.remove("Overflow")
    
    return allFiles


# TODO
def moveFile(file, newPath):
    oldPath = path + file
    shutil.move(oldPath, newPath)
     


files_to_sort = dectectChange(path)

print(files_to_sort)
