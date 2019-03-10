import os
import sys

# This method returns the absolute path of the config file
def get_config_path():
    cwd = os.path.dirname(os.path.realpath(__file__))
    return os.path.join(cwd, 'config.txt')

# This method returns a list of tuples of the data in the config.txt file.
# Tuple[0] is the repo name
# Tuple[1] is the repo path
def parse_config():
    config_path = get_config_path()
    # if the file does not exist, create the file and return an empty list
    if not os.path.exists(config_path):
        try:
            f = open(config_path, 'w')
        except IOError as e:
            print(e)
        f.close()
        return []
        
    with open(config_path, 'r') as config_file:
        tuple_list = []
        for line in config_file:
            lst = line.strip().split("\t")
            tuple_list.append((lst[0], lst[1]))

    return tuple_list

# This method adds a repo and path to the config.txt file.
# If the file does not already exist, it creates it.
# repo_name is the name of the repo
# repo_path is the path to the repo
def add_config(repo_name, repo_path):
    config_path = get_config_path()
    f = open(config_path, 'a')
    f.write(repo_name + "\t" + repo_path + "\n")
    f.close()
