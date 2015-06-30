import unittest
import SuperGLU.Core.Tests.ClassifierEngine_UnitTests as ClassifierEngine_UnitTests
import SuperGLU.Core.Tests.Messaging_UnitTests as Messaging_UnitTests

def TestSuite():
    """
    Returns a TestSuite object that covers the Util module
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    modules = [ClassifierEngine_UnitTests,
               Messaging_UnitTests,
               TaskManager_UnitTests]
    for m in modules:
        suite.addTests(loader.loadTestsFromModule(m))
    return suite


if __name__ == "__main__":
    import sys
    sys.exit(not unittest.TextTestRunner().run(TestSuite()))
