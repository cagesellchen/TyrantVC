import os


def test(text):
    return text + text

# This method creates a new repo
# return 0 if successfully created a repo
def create_repo(reponame):
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
def load_repo(reponame):
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
def get_file_version(commitId, filepath):
    return os.popen("git show " + commitId + ":" + filepath).read()

# This method returns the name, date, and message of every commit
# that modified a given file.
# return data format: [[commit, date, message],[]...]
def get_file_version_history(filename):
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

# Method to see which files have been changed since the last commit.
# returns a list of file names changed
def get_files_changed():
    outlist = os.popen("git diff --name-only").read().splitlines()
    outlist += os.popen("git ls-files --other --exclude-standard").read().splitlines()
    return outlist


# This commit returns the name of every file that was in a given commit
def get_commit(commitId):
    return os.popen("git diff-tree --no-commit-id --name-only -r " + commitId).read().split()