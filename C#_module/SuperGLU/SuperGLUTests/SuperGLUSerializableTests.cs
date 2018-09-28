using Microsoft.VisualStudio.TestTools.UnitTesting;
using SuperGLU;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SuperGLU.Tests
{
    public class MockSerializable : SuperGLU_Serializable
    {
        public int foo
        { get; set; }

        public String bar
        { get; set; }

        private static String FOO_KEY = "foo";
        private static String BAR_KEY = "bar";


        static MockSerializable()
        {
            CLASS_IDS.Add(typeof(MockSerializable).FullName, typeof(MockSerializable));
        }

        public MockSerializable(int foo, String bar ):base()
        {
            this.foo = foo;
            this.bar = bar;
        }


        public MockSerializable () : base()
        {
            this.foo = -1;
            this.bar = null;
        }

        public override bool Equals(object otherObj)
        {
            if (!base.Equals(otherObj))
                return false;

            if (!otherObj.GetType().Equals(typeof(MockSerializable)))
                return false;

            MockSerializable other = (MockSerializable)otherObj;

            if (this.foo != other.foo)
                return false;

            if (!this.bar.Equals(other.bar))
                return false;

            return true;
                
        }


        public override int GetHashCode()
        {
            int result = base.GetHashCode();

            int arbitraryPrimeNumber = 29;

            result = result * arbitraryPrimeNumber + foo.GetHashCode();
            if (bar != null)
                result = result * arbitraryPrimeNumber + bar.GetHashCode();

            return result;
        }


        public override StorageToken saveToToken()
        {
            StorageToken token = base.saveToToken();

            token.setItem(FOO_KEY, this.foo);
            token.setItem(BAR_KEY, this.bar);


            return token;
        }


        public override void initializeFromToken(StorageToken token)
        {
            base.initializeFromToken(token);
            this.foo = (int)SerializationConvenience.untokenizeObject(token.getItem(FOO_KEY, true, -1));
            this.bar = (String)SerializationConvenience.untokenizeObject(token.getItem(BAR_KEY, true, null));
        }




    }



    [TestClass()]
    public class SuperGLUSerializableTests
    {
        [TestMethod()]
        public void CloneTest()
        {
            SuperGLU_Serializable original = new SuperGLU_Serializable("test");
            SuperGLU_Serializable clone = original.clone(false);
            Assert.AreEqual(original, clone);
        }


        [TestMethod()]
        public void TestTokenizeObject()
        {
            MockSerializable obj = new MockSerializable(5, "test");
            StorageToken token = obj.saveToToken();
            MockSerializable copy = (MockSerializable) MockSerializable.createFromToken(token);

            Assert.AreEqual(obj, copy);
        }

    }
}