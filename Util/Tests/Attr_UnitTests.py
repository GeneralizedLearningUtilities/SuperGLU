import unittest

from SuperGLU.Util.Attr import get_prop

class TestGetProp(unittest.TestCase):
    def setUp(self):
        pass
        
    def tearDown(self):
        pass

    def testNoneInputs(self):
        class c(object):
            a = "HERE"
            def __init__(self):
                self.b = "THERE"

        obj = c()

        self.assertEquals("HERE", get_prop(obj, "a"))
        self.assertEquals("THERE", get_prop(obj, "b"))
        
        self.assertIsNone(get_prop(obj, None))
        self.assertIsNone(get_prop(None, "a"))
        self.assertIsNone(get_prop(None, None))

    def testVanilla(self):
        class tester(object):
            def __init__(self):
                self.a = "I am a"
                self._c = "I am _c"
                self.D = "I am D"
                self._F = "I am _F"
            
            def getB(self):
                return "I am getB"
            
            def gete(self):
                return "I am gete"
        
            def deepfunc(self):
                def f1():
                    def f2():
                        return "I am deepfunc o f1 o f2 " + self.a
                    return f2
                return f1
            
            def yielder(self):
                yield "I Yielded"
                
            def yielder2(self):
                def f1():
                    yield "I Yielded in a subfunc"
                return f1
    
        t = tester()
        
        self.assertIsNone(get_prop(t, "XYZ"))
        
        self.assertEquals("I am a", get_prop(t, "a"))
        self.assertEquals("I am getB", get_prop(t, "b"))
        self.assertEquals("I am _c", get_prop(t, "c"))
        self.assertEquals("I am D", get_prop(t, "d"))
        self.assertEquals("I am gete", get_prop(t, "e"))
        self.assertEquals("I am _F", get_prop(t, "f"))
        self.assertEquals("I am deepfunc o f1 o f2 I am a", get_prop(t, "deepfunc"))
        self.assertEquals(["I Yielded"], list(get_prop(t, "yielder")))
        self.assertEquals(["I Yielded in a subfunc"], list(get_prop(t, "yielder2")))
    
    def testList(self):
        class tester(object):
            def __init__(self):
                self.a = ["I am a"]
                self._c = ["I am _c"]
                self.D = ["I am D"]
                self._F = ["I am _F"]
            
            def getB(self):
                return ["I am getB"]
            
            def gete(self):
                return ["I am gete"]
        
            def deepfunc(self):
                def f1():
                    def f2():
                        return ["I am deepfunc o f1 o f2"] + self.a
                    return f2
                return f1
            
            def yielder(self):
                yield "I Yielded"
                
            def yielder2(self):
                def f1():
                    yield "I Yielded in a subfunc"
                return f1
    
        t = tester()
        
        self.assertIsNone(get_prop(t, "XYZ", list))
        
        self.assertEquals(["I am a"], get_prop(t, "a", list))
        self.assertEquals(["I am getB"], get_prop(t, "b", list))
        self.assertEquals(["I am _c"], get_prop(t, "c", list))
        self.assertEquals(["I am D"], get_prop(t, "d", list))
        self.assertEquals(["I am gete"], get_prop(t, "e", list))
        self.assertEquals(["I am _F"], get_prop(t, "f", list))
        self.assertEquals(["I am deepfunc o f1 o f2", "I am a"], get_prop(t, "deepfunc", list))
        self.assertEquals(["I Yielded"], get_prop(t, "yielder", list))
        self.assertEquals(["I Yielded in a subfunc"], get_prop(t, "yielder2", list))

        
