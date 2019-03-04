import os

# This method checks to see if a config.txt file exists in the
# TyrantVC folder. If it doesn't, it creates one.
def init_config():
    os.chdir(os.path.expanduser("~/Library/Preferences/Autodesk/maya/plug-ins/TyrantVC"))
    ls = os.popen("ls").read().splitlines()

    if "config.txt" not in ls:
        os.system("touch config.txt")

# This method returns a list of tuples of the data in the config.txt file.
# Tuple[0] is the repo name
# Tuple[1] is the repo path
def parse_config():
    os.chdir(os.path.expanduser("~/Library/Preferences/Autodesk/maya/plug-ins/TyrantVC"))
    config_txt = os.popen("cat config.txt").read().splitlines()

    tuple_list = []
    for tuple in config_txt:
        lst = tuple.split(" ")
        tuple_list.append((lst[0], lst[1]))

    return tuple_list

# This method adds a repo and path to the config.txt file
# repo_name is the name of the repo
# repo_path is the path to the repo
def add_config(repo_name, repo_path):
    os.chdir(os.path.expanduser("~/Library/Preferences/Autodesk/maya/plug-ins/TyrantVC"))
    f = open("config.txt", "a")
    f.write(str(repo_name) + " " + str(repo_path))
    f.close()