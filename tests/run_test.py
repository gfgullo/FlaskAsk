import unittest
from coverage import coverage

COV = coverage(branch=True, include='../app/*')
COV.start()

tests = unittest.TestLoader().discover('')
unittest.TextTestRunner(verbosity=2).run(tests)

COV.stop()
COV.report()
COV.html_report()

