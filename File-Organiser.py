# Importign nexessary modules
import os           # OS (checking directories) - directory checking & listing
import shutil       # File Operation
import re           # Regex - FileName Manipulation
import csv          # CSV operations - Handling persistent route storage
import threading    # Threading - Allow automatic processing & user input
import time         # Time - Pausing gap in auto processing.


# To set-up ensure these following variables are correct for use. 
startPATH = r"H:\hjgre\Downloads2\DropSort"             # Starting directory to check for updates in files.
automaticInterval = 600                                 # Changing this, changes the interval at which automatic processing occures (beware increasing also increases the time it takes for automatic processing to be stopped/quit).
inpMsg = "Auto-File-Organizer: Command: (h for help): " # Message given to user to interact with system. 

""" Hash Table Implementation """
# Simple node class to store nodes in LL DS (apart of a larger hash table).
class node:
    def __init__(self, data):
        self.data = data
        self.next = None

# Stores all routes in a hash table {containing dictionaries in nodes.} This can then be searched when creating final destination path for a file.
hashmap_size = 100
routes = [None] * hashmap_size

# Adds the route to the hash table (returns nothing and accepts the route dictionary as argument)
def addRoute_toHashTable(route_dict):
    location = hash_function(route_dict['code'])    # Get the cell where the route will be located.
    route = node(route_dict)                        # Create a node out of the dict

    # Handles locating if it is a base node.
    if routes[location] == None:
        routes[location] = route
    else:
        # Linearly search the LL to find the end of the list 
        current = routes[location]
        while current.next is not None:
            current = current.next
        
        # Set the new node on the end of the LL.
        current.next = route

    return

# Accepts a code and returns the int location where that route can be stored.
def hash_function(search_code):
    # Calculates the location for where a route will be stored. 
    total = 0 
    # Iterate over all the letters in the code and add the unicode values togethor
    for letter in search_code:
        total += ord(letter)
    
    code = total % hashmap_size     # Normalise total to be in bounds of hash table arr.
    
    return code

# Accepts a code and returns the path of that route (or Nothing if code is invalid).
def searchHashTable(search_code):
    hash = hash_function(search_code)   # Find which cell the route will be stored in.

    current_node = routes[hash]         # Pointer to first node in LL.

    # Check if there is a valid route as destination:
    if current_node is None:
        return None
    
    # If the first node is the searched for node, then return the path stored in the node.
    if current_node.data['code'] == search_code:
        return current_node.data['path']
    else:
    # Search till the end of the LL is found or the searched for node is found.
        while current_node.next is not None and current_node.data['code'] != search_code:
            current_node = current_node.next
        
        # If the code is not valid (ie end of LL reached, return None).
        if current_node.data is None:
            return None
        else:
        # Return the path for the searched for node.
            return current_node.data['path']


""" Handling CSV """
# Create Dictionary of available routes.
def readCSV():
    # Read all the codes into a dictionary.
    with open(r"E:\Programming\Automatic-File-Organisation\Routes.csv", mode='r') as file:
        reader = csv.DictReader(file)

        # Add each dictionary to the routes list.
        for row in reader:
            addRoute_toHashTable(row)


""" Main Processing of moving files based of codes"""
# Detects any changes to the given PATH (startPATH) and returns a list of all the changed files to be sorted.
def detectChange(path):
    allFiles = os.listdir(path) # Gets all files in the path in a list

    # Clean list
    if "Overflow" in allFiles:
        allFiles.remove("Overflow")
    if "Games" in allFiles:
        allFiles.remove("Games")
    
    return allFiles

# Handles the actual moving of the file from one location to another.
def moveFile(file, newPath):
    # Create original and new path based of parameters.
    oldPath = startPATH + "/" + file
    newPath = newPath + "/" + file

    # Using module to handle physical file move.
    try:
        shutil.move(oldPath, newPath)
    except:
        try:
            newPath = searchHashTable("XX") + "/" + file
            shutil.move(oldPath, newPath)
        except:
            return
    # Return (*to be implemented when securing the program)
    return 

# Checks if a fileName is a directory or not
def is_directory(fileName, path):
    # Check if the fileName is a directory or file 
    fullPath = os.path.join(path, fileName)
    if os.path.isdir(fullPath):
        # File is a directory
        return True
    else:
        return False

# Route the file to correct destination - finds all the codes then finds the path based of the codes.
# Obtains code abreviations from filename.
def obtainCodes(fileName, path): 

    if not is_directory(fileName, path):
        # Remove FileType - mask finds the final full stop and looks ahead to the end of the string.
        mask = r"^(.*)(?=\.[^.]*$)"
        regex_name = re.findall(mask, fileName)
        #
        # vv Should always run due to overarching is_directory check. 
        # If it is a directory will not have a file type so nothing will be picked up in mask. Therefore no change.
        if len(regex_name) != 0:
            fileName = regex_name[0]


    # Obtain Code - Between the last '_' and the end of the string.
    mask = r"\_[^_]*$"
    fileName = re.findall(mask, fileName) 
    if len(fileName) != 0:  
        fileName = fileName[0] # Select first item in list (findall returns list) - findall Returns list.
    else:
        fileName = "_"      # If no codes found in name just create a string so no codes are returned however code doesn't break.

    fileName = fileName[1:] # Remove the _ from the string.

    # Split codes into seperate code in a list (splitting on '-')
    mask = r"[^-]+"

    codes = re.findall(mask, fileName)
    return codes    # Returns list generated by findall

# Processes the codes - finds destination PATH & checks if filename needs cleaning.
def findDestination(codes, filename, filepath):
    # Loop over codes and check if valid code and find path

    # Base Case - if no valid code, move the file to the overflow area for manual processing. 
    # Provided user hasn't changed routes format, this should be the first dict in route therefore Ω(1) as it is first.
    destination = searchHashTable("XX")

    # Find if there is a valid base path
    if len(codes) != 0:
        # Check if the path is a valid code
        path = searchHashTable(codes[0])
        if path is not None:
            # set the destination to the new path.
            destination = path

        # For the rest of the codes in the names, find the path for the code to create the full path.
        for index, code in enumerate(codes):
            if index == 0 or code == "rm":
                continue
            path = searchHashTable(code)

            if path is not None:
                destination += path

    # If rm is present then the filename needs to be cleaned (ie codes removed)
    if "rm" in codes:
        filename = cleanName(filename, filepath)
        return destination, filename, True
    
    # Returns: destination PATH, filename the file should be saved as & if cleanName has been used
    return destination,filename, False

# Cleans File Name.
def cleanName(fileName, path):

    if not is_directory(fileName, path):
        # Locates the codes between final '_' and the file type 
        mask = r"(_[^_]+)(?=\.[^.]*$)"
    else:
        # Locates the codes between final '_' and end of file name
        mask = r"\_[^_]*$" 

    match = re.search(mask, fileName)

    # If codes are found then it is a file and codes should be replaced with "" 
    if match:
        fileName = fileName.replace(match[0], "")
        return fileName
    
    # If provblem occured and nothing is changed than just return the original filename. 
    return fileName

# Runs the full process of finding files to sort, sorting them & renaming them.
def main():
    # Make sure using most-up-to-date routes (ie re-read)
    readCSV()

    # Find a list of files that need to be sorted
    files = detectChange(startPATH)

    # Iterate over each file, locate the codes and subsequent destination 
    for file in files:
        codes = obtainCodes(file, startPATH)
        returns = findDestination(codes, file, startPATH)
        destination = returns[0]; filename = returns[1]; isNameChange = returns[2]

        # Move file to new location
        moveFile(file,destination)

        # Change the name if necessary
        if isNameChange:
            try:
                os.rename((destination + "/" + file), (destination+ "/" + filename))
            except Exception as e:
                print(f"File name has not been cleaned but may still have been relocated: Error Msg: {e}")

    
    print("\r\033[KFiles Processed")


""" THREADING """
# THREADING to run the process yet allowing the user to dictate when to stop it etc.
# Used to stop automatic processing and allow the program to sync.
stop_thread = True

# Used to start the process running automatically every interval (original 10mins).
def automaticRun():
    global stop_thread, automaticInterval      # Ensure edits global scope.
    # While the process has not been stopped by user (will be running in a seperate thread)
    while not stop_thread:
        main()
        # If the stop_thread is set to True this time will run out and the procedure will exit out after timer.
        automaticInterval = automaticInterval / 100
        for i in range(100):
            if not stop_thread:
                time.sleep(automaticInterval) # Wait 10mins
            else:
                break

auto = threading.Thread(target=automaticRun)
# Starts the automatic process on a seperate thread.
def startAutomatic():
    global stop_thread, auto
    stop_thread = False     # Ensure processing does not stop instantly.
    # Creating a new thread that will run the automatic processing. 
    auto = threading.Thread(target=automaticRun)
    auto.start()            # Start the processing on the seperate thread.

# Stops the automatic process.
def stopAutomatic():
    global stop_thread, auto
    stop_thread = True      # This will stop the automatic processing loop.
    auto.join()             # Syncs the program/thread (thread merges & joins main program when finishes)

# Get command for user for next step.
def userInput():
    global auto

    while True:
        # Gain the user's command.
        startupInput = input(inpMsg) 

        if startupInput == "h":   # Output Commands to user to assist with all available commands. 
            print("""Commands: h = help menu giving available commands
            a = start automatic processing.
            s = stops automatic processing.
            m = begin a manual process (stops automatic).
            c = create new route/extension.
            q = quit program.""")

        elif startupInput == "a": # Starts automatic processing.
            if not auto.is_alive():
                print("Type 's' to stop.")
                startAutomatic()
            else:
                print("Already Running")

        elif startupInput == "m": # Switches to manual processing (and does a manual run).
            main()
            if auto.is_alive():
                stopAutomatic()

        elif startupInput == "s": # Stops the automatic process (without quitting program)
            if auto.is_alive():
                print("Stopping Automatic Process...")
                stopAutomatic()
                print("Automatic Process has been stopped")
            else:
                print("Process is not running")

        elif startupInput == "c": # Creates a new route for the program
            # Gains necessary input to create a new path.
            code = input("What is the code for the new route? ")
            desc = input("Give a short description for the path: ")
            path = input("What is the full path to the destination directory for the route?")
            type = input("What is the type of the route (base or extention)? ")

            if code == "" or path == "" or type =="":
                print("Missing Necessary Data")
                continue

            # Check if code is a copy
            readCSV()

            # Checks if the code is a duplicate code.
            if searchHashTable(code) is not None:
                print("Duplicate Code")
                continue
        

            if type == "base":
                # Check base directory is valid.
                if not os.path.exists(path):
                    print("Not a valid PATH")
                    continue
            elif type == "extention":
                base = input("Give the full base path of the base directory for the extention: ")
                # Check the extention path is valid.
                if not os.path.exists(base):
                    print("Not a valid PATH")
                    continue

                else:
                    path = path.replace(base, "")   # Create a valid extention path.
            else:
                print("Please correctly type 'base' or 'extention'.")
                continue

            # *NOTE : DW if string writes without "" shouldn't break it. 

            # Write the new Route to the csv.
            with open('./Routes.csv', mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([code, path, desc, type])
            
            userInput()
            return
        
        elif startupInput == "q": # Quit Application

            # If the automatic process thread is going, then stop it and quit application.
            if auto.is_alive():
                stopAutomatic()
                print("Quitting automatic process.")
            print("Quitting Application")
            return
        
        else:
            continue

# Upon Starting program start by prompting user on what processsing mode they want to use.
userInput()

