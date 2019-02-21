import unittest
import GitAccess
import os
import shutil


class GitAccessTest(unittest.TestCase):
    # name of the repo where tests are performed
    reponame = "testrepo"
    
    # directory of where the test process is running
    basedir = ""

    # list of file names in the test repo
    testFiles = []

    # runs before each test
    def setUp(self):
        # get the directory of the process
        self.basedir = os.getcwd()

        # create the repo
        os.makedirs(self.reponame)
        
        # populate the directory with text files
        for i in range(5):
            filename = "test" + str(i) + ".txt"
            os.system("echo \"test " + str(i) + "\" > " + self.reponame + "/" + filename)
            self.testFiles.append(filename)

    #runs after each test
    def tearDown(self):
        # move to the directory of the repo
        os.chdir(self.basedir)

        # remove everything inside of it
        shutil.rmtree(self.reponame)

    # test whether the unit testing is working
    def test_test(self):
        self.assertEqual(GitAccess.test("test"), "testtest")

    # test whether a repo can successfully be created
    def test_createRepo(self):
        self.assertEqual(GitAccess.createRepo(self.basedir + "/" + self.reponame), 0)

    # test commit a change to a file
    def test_commit(self):
        # create a repo
        GitAccess.createRepo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        fileChanged = self.testFiles[0]
        os.system("echo \"updated\" > " + fileChanged)
        
        self.assertEqual(GitAccess.commit([fileChanged], "update file"), 0)

    # test commit a change to a file
    def test_getFileVersionHistory(self):
        # create a repo
        GitAccess.createRepo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        fileChanged = self.testFiles[0]
        os.system("echo \"updated\" > " + fileChanged)
        
        # commit the change
        GitAccess.commit([fileChanged], "update file")

        print(GitAccess.getFileVersionHistory(fileChanged))



    
if __name__ == '__main__':
    unittest.main()