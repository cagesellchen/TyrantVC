from sys import platform
import os
import getpass
import shutil

## Installationg script for TyrantVC plugin. 
## Drag and drop the script into viewfinder panel in Maya
## to run the script.

# Location of the plugin on github
REPO_NAME = "TyrantVC"
PLUGIN_FILE = "tyrantvc.py"
GIT_PATH = "https://github.com/cagesellchen/" + REPO_NAME + ".git"

def install_tyrantvc():

    # determine which platform we are running on
    if platform == "linux" or platform == "linux2":
        # Linux
        print("TyrantVC is not supported on Linux yet.")  
    elif platform == "darwin":
        # OSX
        retreive_plugin_files(os.environ['HOME'] + "/Library/Preferences/Autodesk/maya/plug-ins") 
    elif platform == "win32" or platform == "win64":
        # Windows
        retreive_plugin_files("\\Users\\" + getpass.getuser() + "\\Documents\\maya\\plug-ins") 

def retreive_plugin_files(maya_plugin_path):
    
    print("Starting installation of TyrantVC.")
    
    # check whether the plugin path exists directory exists
    if not os.path.isdir(maya_plugin_path):
        print("Plugin directory not found. Creating one.")
        os.makedirs(maya_plugin_path)
    
    print("Moving to " + maya_plugin_path)
    os.chdir(maya_plugin_path)
    
    # check whether the plugin is already installed
    if os.path.isdir(REPO_NAME) and os.path.isfile(PLUGIN_FILE):
        print("TyrantVC is already installed, deleting old version.")
        shutil.rmtree(REPO_NAME)
        os.remove(PLUGIN_FILE)

    print("Downloading TyrantVC script files.")

    os.system("git clone " + GIT_PATH)
    
    print("Successfully downloaded TyrantVC.")
    print("Setting up the files.")
    
    os.system("mv " + REPO_NAME + "/" + PLUGIN_FILE + " " + PLUGIN_FILE)  
   
    print("TyrantVC installed!")

def onMayaDroppedPythonFile(arg):
    #print(arg)
    install_tyrantvc()
