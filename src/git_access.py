import os
import subprocess

# Defining startup behavior for the subprocess, this will 
# hide the window that the commands are executed in
si = subprocess.STARTUPINFO()
si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

# Creates a new repo or loads an existing repo from an existing folder
# return 0 if successfully created a repo
def create_repo(reponame):
    # move inside the right directory
    os.chdir(reponame)
    
    # initialize a repo
    res = 0

    # check if the directory has any files in it
    dir_not_empty = len(os.listdir(reponame))
    is_repo = os.path.isdir(".git")
    
    # check if the user.name is set. if not, we give it a local one
    # just for this repo. maya had trouble auto-identifying git user.names sometimes

    # if it is not already a repo, create it
    if not is_repo:
        res = subprocess.call("git init", startupinfo=si)
        
    res = subprocess.call("git config user.name", startupinfo=si)
    if res != 0:
        subprocess.call("git config user.name \"TyrantVC User\"", startupinfo=si)
        subprocess.call("git config user.email \"user@tyrantvc.fake\"", startupinfo=si)
            
    # if there were files in here already, add and commit them now
    if not is_repo and dir_not_empty:
        res = subprocess.call("git add --all", startupinfo=si)
        res = subprocess.call("git commit -m \"first commit\"", startupinfo=si)
                
    return res


# This method adds and commits a list of files
# return commitId if succesfully committed
def commit(filelist, message):
    subprocess.check_output("git add " + " ".join(filelist), startupinfo=si)
    subprocess.check_output("git commit -m " + "\"" + message + "\"", startupinfo=si)

    commitId = subprocess.check_output("git rev-parse HEAD", startupinfo=si).splitlines()[0]
    return commitId


# This method returns the code for a specific version of a file
# filename must be a path to the given file
def get_file_version(commitId, filepath):
    return subprocess.check_output("git show " + commitId + ":" + filepath, startupinfo=si)

# This method returns the name, date, and message of every commit
# that modified a given file.
# return data format: [[commit, date, message],[]...]
def get_file_version_history(filename):
    outlist = subprocess.check_output("git log --follow -- " + filename, startupinfo=si).splitlines()
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
    outlist = subprocess.check_output("git diff --name-only", startupinfo=si).splitlines()
    outlist += subprocess.check_output("git ls-files --other --exclude-standard", startupinfo=si).splitlines()
    return outlist


# Returns the name of every file that was in a given commit
def get_committed_files(commitId):
    return subprocess.check_output("git diff-tree --no-commit-id --name-only -r " + commitId, startupinfo=si).split()



# Returns every commit in a tuple: (commit_id, date, message, files)
# date is in Date format; ex: 'Tue Mar 5 10:16:30 2019 -0800'
# files is a list of files; ex: ['src/config_access.py', 'src/main_panel.py']
def get_all_commits():
    outlist = subprocess.check_output("git log --pretty=format:\"%H\\t%ad\\t%s\" -100", startupinfo=si).splitlines()

    data = []
    for line in outlist:
        lst = line.strip().split("\t")
        data.append((lst[0], lst[1], lst[2], get_committed_files(lst[0])))

    return data
