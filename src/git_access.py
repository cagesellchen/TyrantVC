import os
import subprocess
import platform


# Creates a new repo or loads an existing repo from an existing folder
# return 0 if successfully created a repo
def create_repo(reponame):
    # label for telling run_os_dependent_command() to use the subprocess.call method
    use_call_method = True

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
        # res = subprocess.call("git init", startupinfo=si)
        res = run_os_dependent_command("git init", use_call_method)
        
    res = run_os_dependent_command("git config user.name", use_call_method)
    if res != 0:
        run_os_dependent_command("git config user.name \"TyrantVC User\"", use_call_method)
        run_os_dependent_command("git config user.email \"user@tyrantvc.fake\"", use_call_method)
            
    # if there were files in here already, add and commit them now
    if not is_repo and dir_not_empty:
        res = run_os_dependent_command("git add --all", use_call_method)
        res = run_os_dependent_command("git commit -m \"first commit\"", use_call_method)
                
    return res


# This method adds and commits a list of files
# return commitId if succesfully committed
def commit(filelist, message):
    run_os_dependent_command("git add " + " ".join(filelist))
    run_os_dependent_command("git commit -m " + "\"" + message + "\"")

    commit_id = run_os_dependent_command("git rev-parse HEAD").splitlines()[0]
    return commit_id


# This method returns the code for a specific version of a file
# filename must be a path to the given file
def get_file_version(commitId, filepath):
    return run_os_dependent_command("git show " + commitId + ":" + filepath)

# This method returns the name, date, and message of every commit
# that modified a given file.
# return data format: [[commit, date, message],[]...]
def get_file_version_history(filename):
    outlist = run_os_dependent_command("git log --follow -- " + filename).decode('ascii').splitlines()


    outlist.append("")  # last commit entry doesn't have a blank line after it
                        # resulting in one less line than the other entries

    data = []
    for i in range(int(len(outlist)/6)):
        commit_id = outlist[i*6][7:]  # removing "commit: " text
        date = outlist[i*6 + 2][8:]  # removing "date: " text & tab
        message = outlist[i*6 + 4][4:]  # removing tab
        data.append([commit_id, date, message])

    return data

# Method to see which files have been changed since the last commit.
# returns a list of file names changed
def get_files_changed():
    outlist = run_os_dependent_command("git diff --name-only").splitlines()
    outlist += run_os_dependent_command("git ls-files --other --exclude-standard").splitlines()

    return outlist


# Returns the name of every file that was in a given commit
def get_committed_files(commitId):
    return run_os_dependent_command("git diff-tree --no-commit-id --name-only --root -r " + commitId).split()


# Returns every commit in a tuple: (commit_id, date, message, files)
# date is in Date format; ex: 'Tue Mar 5 10:16:30 2019 -0800'
# files is a list of files; ex: ['src/config_access.py', 'src/main_panel.py']
def get_all_commits():
    outlist = run_os_dependent_command("git log --pretty=format:\"%H\t%ad\t%s\" -100").splitlines()

    data = []
    for line in outlist:
        lst = line.strip().split("\t")
        data.append((lst[0], lst[1], lst[2], get_committed_files(lst[0])))

    return data


# returns the proper call for a command based on the user's OS
# 'command' parameter is the git command to be run
# 'is_call' parameter is true if you want to use subprocess.call,
#       vs false if you want to use subprocess.check_output
def run_os_dependent_command(command, is_call=False):
    if platform.system() == "Windows":
        # Defining startup behavior for the subprocess, this will
        # hide the window that the commands are executed in
        si = subprocess.STARTUPINFO()
        si.dwFlags |= subprocess.STARTF_USESHOWWINDOW

        if is_call:
            return subprocess.call(command, startupinfo=si)
        else:
            # decode because subprocess returns data in bytes
            return subprocess.check_output(command, startupinfo=si).decode('ascii')
    else:
        if is_call:
            return subprocess.call(command, shell=True)
        else:
            # decode because subprocess returns data in bytes
            return subprocess.check_output(command, shell=True).decode('ascii')
