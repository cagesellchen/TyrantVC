import os


def test(text):
    return text + text

# This method creates a new repo
# return 0 if successfully created a repo
def createRepo(reponame):
    # move inside the right directory
    os.chdir(reponame)
    
    # try to initialize a repo
    success = os.system("git init")
    
    # if succsefully initialized, add all the files and commit them
    if success == 0:
        success = os.system("git add --all")
        success = os.system("git commit -m \"first commit\"")
    
    return success


# This method loads a repo
# return None
def loadRepo(reponame):
    os.system("cd " + reponame)
    return None


# This method adds and commits a list of files
# return 0 if succesfully committed
def commit(filelist, message):
    success = os.system("git add " + " ".join(filelist))
    success = os.system("git commit -m " + "\"" + message + "\"")
    return success


# This method returns the code for a specific version of a file
# filename must be a path to the given file
def getFileVersion(commitId, filepath):
    return os.popen("git show " + commitId + ":" + filepath).read()

# This method returns the name, date, and message of every commit
# that modified a given file.
# return data format: [[commit, date, message],[]...]
def getFileVersionHistory(filename):
    outlist = os.popen("git log --follow -- " + filename).read().splitlines()
    outlist.append("")  # last commit entry doesn't have a blank line after it
                        # resulting in one less line than the other entries

    data = []
    for i in range(int(len(outlist)/6)):
        commitId = outlist[i*6][7:]  # removing "commit: " text
        date = outlist[i*6 + 2][8:]  # removing "date: " text & tab
        message = outlist[i*6 + 4][4:]  # removing tab
        data.append([commitId, date, message])

    return data


# This commit returns the name of every file that was in a given commit
def getCommit(commitId):
    return os.popen("git diff-tree --no-commit-id --name-only -r " + commitId).read().split()


def main():
    # commit(["GitAccess.py"], "Testing Commit from a Python File")
    # getFileVersion("27819af5d2f0bea526e1c177feb08f68563839c0", "BackEnd/GitAccess.py")
    # print(getFileVersionHistory("GitAccess.py"))
    print(getCommit("27819af5d2f0bea526e1c177feb08f68563839c0"))


if __name__ == '__main__':
    main()