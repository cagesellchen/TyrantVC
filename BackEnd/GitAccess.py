import os

# filelist is a list of files to be committed
def commit(filelist, message):
    os.system("git add " + " ".join(filelist))
    os.system("git commit -m " + "\"" + message + "\"")
    os.system("git push")


def main():
    commit(["GitAccess.py"], "Testing Commit from a Python File")


if __name__ == '__main__':
    main()