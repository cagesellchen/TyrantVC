import os

# This method creates a new repo and
def createRepo(reponame):
    return None


# This method returns the files in a repo to populate
# the file/commit browser (???)
def loadRepo(reponame):
    return None


# This method adds and commits a list of files
def commit(filelist, message):
    os.system("git add " + " ".join(filelist))
    os.system("git commit -m " + "\"" + message + "\"")


# This method returns the code for a specific version of a file
# filename must be a path to the given file
def getFileVersion(commit, filepath):
    return os.popen("git show " + commit + ":" + filepath).read()

# This method returns the name, date, and message of every commit
# that modified a given file.
# return data format: [[commit, date, message],[]...]
def getFileVersionHistory(filename):
    outlist = os.popen("git log --follow -- " + filename).read().splitlines()
    outlist.append("")  # last commit entry doesn't have a blank line after it
                        # resulting in one less line than the other entries

    data = []
    for i in range(int(len(outlist)/6)):
        commit = outlist[i*6][7:]
        date = outlist[i*6 + 2][8:]
        message = outlist[i*6 + 4][4:]
        data.append([commit, date, message])

    return data


# This commit returns the name of every file that was modified in
# a given commit
def getCommit(commit):
    return None



def main():
    # commit(["GitAccess.py"], "Testing Commit from a Python File")
    # getFileVersion("27819af5d2f0bea526e1c177feb08f68563839c0", "BackEnd/GitAccess.py")
    getFileVersionHistory("GitAccess.py")


if __name__ == '__main__':
    main()