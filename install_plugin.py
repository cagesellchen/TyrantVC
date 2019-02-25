from sys import platform
if platform == "linux" or platform == "linux2":
    # linux
    print("linux")
elif platform == "darwin":
    # OS X
    print("osx")
elif platform == "win32":
    # Windows...
    print("win32")