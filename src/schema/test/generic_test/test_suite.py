import unittest

loader = unittest.TestLoader()
suite = loader.discover(start_dir='./', pattern='*_test.py')

runner = unittest.TextTestRunner()
runner.run(suite)
