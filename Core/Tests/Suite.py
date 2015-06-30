import unittest
import SKO_Architecture.Tests.ClassifierEngine_UnitTests as ClassifierEngine_UnitTests
import SKO_Architecture.Tests.Messaging_UnitTests as Messaging_UnitTests
import SKO_Architecture.Tests.TaskManager_UnitTests as TaskManager_UnitTests

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
