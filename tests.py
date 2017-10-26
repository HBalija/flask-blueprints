#!/usr/bin/env python

import coverage
import unittest

# define coverage to check app module
c = coverage.coverage(branch=True, include='app/*')
c.start()

# discover finds tests in 'tests' folder
suite = unittest.TestLoader().discover('app/tests')
unittest.TextTestRunner(verbosity=2).run(suite)

c.stop()
c.report()
