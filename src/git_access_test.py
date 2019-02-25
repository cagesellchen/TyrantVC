import unittest
import git_access
import os
import shutil


class git_access_test(unittest.TestCase):
    # name of the repo where tests are performed
    reponame = "testrepo"
    
    # directory of where the test process is running
    basedir = ""

    # list of file names in the test repo
    test_files = []

    # runs before each test
    def setUp(self):
        print("setting up")
        # get the directory of the process
        self.basedir = os.getcwd()

        # create the repo
        os.makedirs(self.reponame)
        
        # populate the directory with text files
        for i in range(5):
            filename = "test" + str(i) + ".txt"
            os.system("echo \"test " + str(i) + "\" > " + self.reponame + "/" + filename)
            self.test_files.append(filename)

    #runs after each test
    def tearDown(self):
        # move to the directory of the repo
        os.chdir(self.basedir)

        # remove everything inside of it
        shutil.rmtree(self.reponame)

    # test whether the unit testing is working
    def test_test(self):
        self.assertEqual(git_access.test("test"), "testtest")

    # test whether a repo can successfully be created
    def test_create_repo(self):
        self.assertEqual(git_access.create_repo(self.basedir + "/" + self.reponame), 0)

    # test commit a change to a file
    def test_commit(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        fileChanged = self.test_files[0]
        os.system("echo \"updated\" > " + fileChanged)
        
        self.assertEqual(git_access.commit([fileChanged], "update file"), 0)

    # test commit a change to a file
    def test_get_file_version_history(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        file_changed = self.test_files[0]
        os.system("echo \"updated\" > " + file_changed)
        
        # commit the change
        git_access.commit([file_changed], "update file")

        print(git_access.get_file_version_history(file_changed))
    
if __name__ == '__main__':
    unittest.main()