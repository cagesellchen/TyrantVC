import unittest
import GitAccess

class GitAccessTest(unittest.TestCase):

    def test_test(self):
        self.assertEqual(GitAccess.test("test"), "testtest")

if __name__ == '__main__':
    unittest.main()