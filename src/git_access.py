import os

# Creates a new repo or loads an existing repo from an existing folder
# return 0 if successfully created a repo
def create_repo(reponame):
    # move inside the right directory
    os.chdir(reponame)
    
    # initialize a repo
    success = 0

    empty_dir_flag = len(os.listdir(reponame))

    if not os.path.isdir(".git"):
        success = os.system("git init")
        
        if empty_dir_flag:
            success = os.system("git add --all")
            success = os.system("git commit -m \"first commit\"")
    
    return success


# This method adds and commits a list of files
# return 0 if succesfully committed
def commit(filelist, message):
    os.system("git add " + " ".join(filelist))
    os.system("git commit -m " + "\"" + message + "\"")
    commitId = os.popen("git rev-parse HEAD").read().splitlines()[0]
    return commitId


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


# Returns the name of every file that was in a given commit
def get_committed_files(commitId):
    return os.popen("git diff-tree --no-commit-id --name-only -r " + commitId).read().split()


# Returns every commit in a tuple: (commit_id, date, message, files)
# date is in Date format; ex: 'Tue Mar 5 10:16:30 2019 -0800'
# files is a list of files; ex: ['src/config_access.py', 'src/main_panel.py']
def get_all_commits():
    outlist = os.popen("git log --pretty=format:\"%H\t%ad\t%s\" -100").read().splitlines()

    data = []
    for line in outlist:
        lst = line.strip().split("\t")
        data.append((lst[0], lst[1], lst[2], get_committed_files(lst[0])))

    return data
