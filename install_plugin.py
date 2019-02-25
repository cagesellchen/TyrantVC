from sys import platform
import os
if platform == "linux" or platform == "linux2":
    # linux
    print("TyrantVC is incompatible with Linux operating system.")
elif platform == "darwin":
    # OS X
    print("Installing TyrantVC on OSX...")
    if(not os.path.isdir("/Users/Shared/Autodesk/maya/plug-ins")):
        os.makedirs("/Users/Shared/Autodesk/maya/plug-ins")
    os.chdir("/Users/Shared/Autodesk/maya/plug-ins")
    print("Downloading TyrantVC...")
    os.system("git clone https://github.com/cagesellchen/TyrantVC.git")
    print("Successfully download TyrantVC...\nSetting up the files...")
    os.system("mv TyrantVC/tyrantvc.py tyrantvc.py")
    print("TyrantVC installed! Please restart Maya and search for \"tyrantvc\" in the Plug-In Manager.")
    
elif platform == "win32" or platform == "win64":
    # Windows...
    print("Installing TyrantVC on Windows...")
    if(not os.path.isdir("C:\\Users\\" + str(os.getlogin()) + "\\Documents\\maya\\2019\\plug-ins")):
        os.makedirs("C:\\Users\\" + str(os.getlogin()) + "\\Documents\\maya\\2019\\plug-ins")
    os.chdir("C:\\Users\\" + str(os.getlogin()) + "\\Documents\\maya\\2019\\plug-ins")
    print("Downloading TyrantVC...")
    os.system("git clone https://github.com/cagesellchen/TyrantVC.git")
    print("Successfully download TyrantVC...\nSetting up the files...")
    os.system("mv TyrantVC/tyrantvc.py tyrantvc.py")
    print("TyrantVC installed! Please restart Maya and search for \"tyrantvc\" in the Plug-In Manager.")