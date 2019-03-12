import unittest
import os
import config_access

# config_access_test method coverage

# (1) - get_config_path() 
# (4) - parse_config()
# (3) - add_config(repo_name, repo_path)

class git_access_test(unittest.TestCase):

    # runs before each test
    # def setUp(self):
    
    config_path = os.path.dirname(os.path.realpath(__file__)) + "/config.txt"


    # runs after each test
    def tearDown(self):
        if os.path.exists(self.config_path):
            os.remove(self.config_path)


    ## --------------------------------------------------------------------------------------------
    ## get_config_path tests
    ## --------------------------------------------------------------------------------------------

    # test whether the config path is correct
    def test_get_config_path(self):
        self.assertEqual(config_access.get_config_path(), self.config_path)

    ## --------------------------------------------------------------------------------------------
    ## parse_config tests
    ## --------------------------------------------------------------------------------------------

    # test whether when there is no config file, parse_config creates it
    def test_parse_config_no_config_create_file(self):
        config_access.parse_config()
        self.assertTrue(os.path.exists(self.config_path))

    # test whether when there is no config file, parse_config creates an empty one
    def test_parse_config_no_config_no_paths(self):
        projects = config_access.parse_config()
        self.assertEqual(len(projects), 0)

    # test whether when there is no config file, parse_config creates an empty one
    def test_parse_config_one_path(self):
        config_access.parse_config()

        config_path = config_access.get_config_path()
        f = open(config_path, 'a')
        f.write("repo1\tpath1\n")
        f.close()

        projects = config_access.parse_config()
        self.assertEqual(projects, [('repo1', 'path1')])

    # test whether when there is no config file, parse_config creates an empty one
    def test_parse_config_multi_path(self):
        config_access.parse_config()

        config_path = config_access.get_config_path()
        f = open(config_path, 'a')
        f.write("repo1\tpath1\n")
        f.write("repo2\tpath2\n")
        f.close()

        projects = config_access.parse_config()
        self.assertEqual(projects, [('repo1', 'path1'),('repo2','path2')])

    ## --------------------------------------------------------------------------------------------
    ## add_config tests
    ## --------------------------------------------------------------------------------------------

    # test whether adding a single project to config works correctly
    def test_add_config_single_project(self):
        config_access.add_config("repo1", "path1")

        projects = config_access.parse_config()
        self.assertEqual(projects, [('repo1', 'path1')])

    # test whether adding a multiple projects to config works correctly
    def test_add_config_multi_project(self):
        config_access.parse_config()

        config_access.add_config("repo1", "path1")
        config_access.add_config("repo2", "path2")

        projects = config_access.parse_config()
        self.assertEqual(projects, [('repo1', 'path1'),('repo2', 'path2')])

    # test whether adding a multiple projects to config works correctly
    def test_add_config_multi_project_dup_projects(self):
        config_access.parse_config()

        config_access.add_config("repo1", "path1")
        config_access.add_config("repo2", "path2")
        config_access.add_config("repo2", "path2")

        projects = config_access.parse_config()
        self.assertEqual(projects, [('repo1', 'path1'),('repo2', 'path2'), ('repo2', 'path2')])


    
if __name__ == '__main__':
    unittest.main()
