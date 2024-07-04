# Automatic-File-Organisation
Automatically organises and sorts files placed in a directory and routes across to specific destination on drive depending on code. Allows for routing codes to be removed to ensure filenames are kept 'clean' and understandable.

# Setting up & Using:

Before Using:

    - If you want the program to run on start download to a memorable place, and then run on start through windows
    - Update 'startPATH' with the PATH of the folder/directory that will be checked for changes and will be checked for files to be sorted (suggested: change it to desktop)
    - Update Routes.csv with all your desired routes, this can be done manually or through CLI
        - DO NOT remove the first and last route 'XX' or 'rm' as this is used by the program.
        - 'rm' cleans the name of the file so the routing codes are removed after the file is moved.
        - 'XX' stores the overflow directory location (ie if a file cannot be sorted anywhere else due to an incorrect code etc, it will be moved it for manual sorting by user.)
        - NOTE: Codes can be uppercase or lowercase and can be any length. 2/3 uppercase letters are suggested for efficiency.

How to use:

    - On start use the command 'h' to show all the available commands.
    - Use 'c' to create new route (follow the steps provided).
    - Choose your operation mode either 'a' (Automatic) or 'm' (Manual)
        - Automatic is better if you want to forget it's running however will continue to be processing
        - Manual is better if you dont want the program to be constantly processing or if you want to force the next processing before the automatic (this will stop the automatic processing)
    - Put a file or folder into your chosen startPATH location (ie desktop), then upon a manual processing or automatic processing, the file will be routed to the location & name will be changed if 'rm' used.
    - When saving a file to the location or moving it, rename it to include the code, codes should come at the end of a file/folder name (but before file-type if relevant).
        - Code should start with '_' 
        - The first code should be either base code (base path)
        - Codes should be seperated with '-'
        - EG FILENAME_base-extention-extention-rm.txt
        - or FILENAME_base-rm.txt 
        - ^^ both valid options

BEWARE: Program has not been stress tested & is not secure so errors likely to occur if program not used properly. Ensure correct usage

Note: System uses threading and batch operation interval: For automatic: 10mins, For manual: up to user.

# 🔮 Future:

*Have startPATH blank on main branch & routes empty except XX, rm, and an example

Future Features:

    - Automatically starts automatic processing if user does not respond.
    - More efficient route searching.
    - Protecting code to prevent crashing or errors.
    - 
