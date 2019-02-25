import unittest

loader = unittest.TestLoader()
start_dir = 'src'
suite = loader.discover(start_dir, pattern="*test.py")

runner = unittest.TextTestRunner()
runner.run(suite)