import unittest
import git_access
import os
import shutil


# git_access_test method coverage

# (4) - create_repo(reponame) 
# (3) - commit(filelist, message)
# (3) - get_file_version(commitId, filepath)
# (1) - get_file_version_history(filename)
# (3) - get_files_changed()
# (2) - get_committed_files(commitId)


class git_access_test(unittest.TestCase):
    # name of the repo where tests are performed
    reponame = "testrepo"
    empty_reponame = "empty"
    
    # directory of where the test process is running
    basedir = ""

    # list of file names in the test repo
    test_files = []

    # runs before each test
    def setUp(self):
        # get the directory of the process
        self.basedir = os.getcwd()

        # create the repo
        os.makedirs(self.reponame)
        os.makedirs(self.empty_reponame)
        
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
        shutil.rmtree(self.empty_reponame)


    ## --------------------------------------------------------------------------------------------
    ## create_repo tests
    ## --------------------------------------------------------------------------------------------

    # test whether a repo can successfully be created from a nonrepo folder with no files
    def test_create_repo_empty_folder_not_repo(self):
        self.assertEqual(git_access.create_repo(self.basedir + "/" + self.empty_reponame), 0)

    # test whether a repo can successfully be created from a repo folder with no files
    def test_create_repo_empty_folder_is_repo(self):
        git_access.create_repo(self.basedir + "/" + self.empty_reponame)
        self.assertEqual(git_access.create_repo(self.basedir + "/" + self.empty_reponame), 0)

    # test whether a repo can successfully be created from a nonrepo folder with files
    def test_create_repo_reg_folder_not_repo(self):
        self.assertEqual(git_access.create_repo(self.basedir + "/" + self.reponame), 0)

    # test whether a repo can successfully be created from a repo folder with files
    def test_create_repo_reg_folder_is_repo(self):
        git_access.create_repo(self.basedir + "/" + self.reponame)
        self.assertEqual(git_access.create_repo(self.basedir + "/" + self.reponame), 0)

    ## --------------------------------------------------------------------------------------------
    ## commit and get_file_version tests
    ## --------------------------------------------------------------------------------------------

    # test commit a change to a file
    def test_commit_get_file_version_single_file(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        fileChanged = self.test_files[0]
        os.system("echo \"updated\" > " + fileChanged)

        commitId = git_access.commit([fileChanged], "update file")
        
        self.assertEqual(git_access.get_file_version(commitId, fileChanged), "updated\n")

    # test committing multiple files at once
    def test_commit_get_file_version_multi_files_single_commit(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        filesChanged = [self.test_files[0],self.test_files[1]]
        os.system("echo \"updated1\" > " + filesChanged[0])
        os.system("echo \"updated2\" > " + filesChanged[1])

        commitId = git_access.commit(filesChanged, "update file")
        
        self.assertEqual(git_access.get_file_version(commitId, filesChanged[0]), "updated1\n")
        self.assertEqual(git_access.get_file_version(commitId, filesChanged[1]), "updated2\n")

    # test committing multiple files in multiple commits
    def test_commit_get_file_version_multi_files_multi_commit(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        filesChanged = [self.test_files[0],self.test_files[1]]
        os.system("echo \"updated1\" > " + filesChanged[0])
        os.system("echo \"updated2\" > " + filesChanged[1])

        commitId1 = git_access.commit([filesChanged[0]], "update file 1")
        commitId2 = git_access.commit([filesChanged[1]], "update file 2")
        
        self.assertEqual(git_access.get_file_version(commitId1, filesChanged[0]), "updated1\n")
        self.assertEqual(git_access.get_file_version(commitId2, filesChanged[1]), "updated2\n")

    ## --------------------------------------------------------------------------------------------
    ## get_files_changed tests
    ## --------------------------------------------------------------------------------------------

    # test not modifying files and seeing whether any changes were detected
    def test_get_files_changed_no_changes(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)
        
        self.assertEqual(git_access.get_files_changed(), [])

    # test modifying a single file and seeing whether the changes were detected
    def test_get_files_changed_single_files(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        filesChanged = [self.test_files[0]]
        os.system("echo \"updated\" > " + filesChanged[0])
        
        self.assertEqual(git_access.get_files_changed(), filesChanged)

    # test modifying multiple files and seeing whether the changes were detected
    def test_get_files_changed_multi_files(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        filesChanged = [self.test_files[0],self.test_files[1]]
        os.system("echo \"updated\" > " + filesChanged[0])
        os.system("echo \"updated\" > " + filesChanged[1])
        
        self.assertEqual(git_access.get_files_changed(), filesChanged)

    ## --------------------------------------------------------------------------------------------
    ## get_file_version_history tests
    ## --------------------------------------------------------------------------------------------

    # test commit a change to a file and seeing that commit in history
    def test_get_file_version_history(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        file_changed = self.test_files[0]
        os.system("echo \"updated\" > " + file_changed)
        
        # commit the change
        git_access.commit([file_changed], "update file")

        # TODO: figure out how to create the timestamp to test using assertEquals
        print(git_access.get_file_version_history(file_changed))

    ## --------------------------------------------------------------------------------------------
    ## get_committed_files tests
    ## --------------------------------------------------------------------------------------------

    # test single file commit
    def test_get_committed_files_single_file(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        fileChanged = self.test_files[0]
        os.system("echo \"updated\" > " + fileChanged)

        commitId = git_access.commit([fileChanged], "update file")
        
        self.assertEqual(git_access.get_committed_files(commitId), [fileChanged])

    # test multiple file commit
    def test_get_committed_files_multi_file(self):
        # create a repo
        git_access.create_repo(self.basedir + "/" + self.reponame)

        # apply a change to a file
        filesChanged = [self.test_files[0],self.test_files[1]]
        os.system("echo \"updated\" > " + filesChanged[0])
        os.system("echo \"updated\" > " + filesChanged[1])
        
        commitId = git_access.commit(filesChanged, "update file")

        self.assertEqual(git_access.get_committed_files(commitId), filesChanged)

    
if __name__ == '__main__':
    unittest.main()