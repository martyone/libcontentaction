#!/usr/bin/python2.5
##
## Copyright (C) 2008, 2009 Nokia. All rights reserved.
##
## Contact: Marius Vollmer <marius.vollmer@nokia.com>
##
## This library is free software; you can redistribute it and/or
## modify it under the terms of the GNU Lesser General Public License
## version 2.1 as published by the Free Software Foundation.
##
## This library is distributed in the hope that it will be useful, but
## WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
## Lesser General Public License for more details.
##
## You should have received a copy of the GNU Lesser General Public
## License along with this library; if not, write to the Free Software
## Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
## 02110-1301 USA

import sys
import os
# Otherwise env.py won't be found when running tests inside a VPATH build dir
sys.path.insert(0, os.getcwd())

try: import env
except: pass

import unittest
from commands import getstatusoutput
from cltool import CLTool
from tempfile import mkdtemp
from shutil import rmtree

# Killing XDG_DATA_DIRS is normally not a good idea, but here we don't need
# any "determining mime type of file" functionalities.
os.environ["XDG_DATA_DIRS"] = os.environ["XDG_DATA_HOME"]

class Defaults(unittest.TestCase):
    def setUp(self):
        os.environ["XDG_DATA_HOME"] = mkdtemp(dir = ".")
        os.mkdir(os.environ["XDG_DATA_HOME"] + "/applications")
    def tearDown(self):
        rmtree(os.environ["XDG_DATA_HOME"])
        
    def testSettingDefault(self):
        (status, output) = getstatusoutput("lca-tool --setmimedefault text/plain foo")
        self.assert_(status == 0)

        (status, output) = getstatusoutput("lca-tool --mimedefault text/plain")
        self.assert_(status == 0)
        self.assert_(output.find("foo") != -1)

    def testDefaultIsFirst(self):
        (status, output) = getstatusoutput("lca-tool --setmimedefault text/plain foo")
        self.assert_(status == 0)
        (status, output) = getstatusoutput("lca-tool --actionsformime text/plain")

        self.assert_(status == 0)
        self.assert_(output.find("foo") < output.find("uberdui"))
        self.assert_(output.find("foo") < output.find("ubermimeopen"))
        self.assert_(output.find("foo") < output.find("uberexec"))

    def testResettingDefault(self):
        # check what are the actions (in order) before
        (status, oldactions) = getstatusoutput("lca-tool --actionsformime text/plain")
        self.assert_(status == 0)

        (status, output) = getstatusoutput("lca-tool --setmimedefault text/plain foo")
        self.assert_(status == 0)

        (status, output) = getstatusoutput("lca-tool --resetmimedefault text/plain")
        self.assert_(status == 0)

        (status, newactions) = getstatusoutput("lca-tool --actionsformime text/plain")
        self.assert_(status == 0)
        self.assert_(newactions == oldactions)

def runTests():
    suite = unittest.TestLoader().loadTestsFromTestCase(Defaults)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return len(result.errors + result.failures)

if __name__ == "__main__":
    sys.exit(runTests())
