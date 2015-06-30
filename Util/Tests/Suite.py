import unittest
import SuperGLU.Util.Tests.TestGenerator_UnitTests as TestGenerator_UnitTests
import SuperGLU.Util.Tests.Serialization_UnitTests as Serialization_UnitTests

def TestSuite():
    """
    Returns a TestSuite object that covers the Util module
    """
    suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    modules = [TestGenerator_UnitTests,
               Serialization_UnitTests]
    for m in modules:
        suite.addTests(loader.loadTestsFromModule(m))
    return suite


if __name__ == "__main__":
    import sys
    sys.exit(not unittest.TextTestRunner().run(TestSuite()))
