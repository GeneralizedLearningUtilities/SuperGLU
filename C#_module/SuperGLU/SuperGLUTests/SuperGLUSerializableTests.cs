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


    public class MockSerializable2 : SuperGLU_Serializable
    {
        public int foo
        { get; set; }

        public String bar
        { get; set; }

        public List<String> baz
        { get; set; }

        public Dictionary<string, string> dict
        { get; set; }

        public MockSerializable nestedSerializable
        { get; set; }

        private static String DICT_KEY = "dict";
        private static String FOO_KEY = "foo";
        private static String BAR_KEY = "bar";
        private static String BAZ_KEY = "baz";
        private static String NESTED_KEY = "nested";
       

        public MockSerializable2(int foo, String bar, List<String> baz, Dictionary<String, String> dict, MockSerializable nested) : base()
        {
            this.foo = foo;
            this.bar = bar;
            this.baz = baz;
            this.dict = dict;
            this.nestedSerializable = nested;
        }


        public MockSerializable2() : base()
        {
            this.foo = -1;
            this.bar = null;
            this.baz = new List<string>();
            this.dict = new Dictionary<string, string>();
            this.nestedSerializable = null;
        }

        public override bool Equals(object otherObj)
        {
            if (!base.Equals(otherObj))
                return false;

            if (!otherObj.GetType().Equals(typeof(MockSerializable2)))
                return false;

            MockSerializable2 other = (MockSerializable2)otherObj;

            if (this.foo != other.foo)
                return false;

            if (!this.bar.Equals(other.bar))
                return false;

            if (!this.baz.SequenceEqual<String>(other.baz))
                return false;

            bool dictionariesEqual = this.dict.Keys.Count == other.dict.Keys.Count && 
                   this.dict.Keys.All(k => other.dict.ContainsKey(k) && object.Equals(this.dict[k], other.dict[k]));

            if (!dictionariesEqual)
                return false;

            if (!nestedSerializable.Equals(other.nestedSerializable))
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

            if (baz != null)
                result = result * arbitraryPrimeNumber + baz.GetHashCode();

            if (dict != null)
                result = result * arbitraryPrimeNumber + dict.GetHashCode();

            if (nestedSerializable != null)
                result = result * arbitraryPrimeNumber + nestedSerializable.GetHashCode();

            return result;
        }


        public override StorageToken saveToToken()
        {
            StorageToken token = base.saveToToken();

            token.setItem(FOO_KEY, this.foo);
            token.setItem(BAR_KEY, this.bar);
            token.setItem(BAZ_KEY, SerializationConvenience.tokenizeObject(this.baz));

            Dictionary<Object, Object> objectDict = new Dictionary<Object, Object>();
            foreach(String key in dict.Keys)
            {
                objectDict.Add(key, dict[key]);
            } 

            token.setItem(DICT_KEY, SerializationConvenience.tokenizeObject(objectDict));
            token.setItem(NESTED_KEY, SerializationConvenience.tokenizeObject(this.nestedSerializable));

            return token;
        }


        public override void initializeFromToken(StorageToken token)
        {
            base.initializeFromToken(token);
            this.foo = (int)SerializationConvenience.untokenizeObject(token.getItem(FOO_KEY, true, -1));
            this.bar = (String)SerializationConvenience.untokenizeObject(token.getItem(BAR_KEY, true, null));
            List<Object> bazAsObjectList = (List<Object>)SerializationConvenience.untokenizeObject(token.getItem(BAZ_KEY, true, new List<Object>()));
            this.baz = new List<string>();
            this.baz.AddRange(bazAsObjectList.Cast<String>());

            Dictionary<Object, Object> nestedAsObjectDict = (Dictionary<Object, Object>)SerializationConvenience.untokenizeObject(token.getItem(DICT_KEY, true, new Dictionary<Object, Object>()));
            this.dict = new Dictionary<string, string>();
            foreach(Object key in nestedAsObjectDict.Keys)
            {
                this.dict.Add((String)key, (String)nestedAsObjectDict[key]);
            }

            this.nestedSerializable = (MockSerializable) SerializationConvenience.untokenizeObject(token.getItem(NESTED_KEY, true, null));
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

        [TestMethod()]
        public void TestTokenizeListObject()
        {
            List<String> stringList = new List<string>();
            stringList.Add("Penguins");
            stringList.Add("birds");

            Dictionary<String, String> dict = new Dictionary<string, string>();
            dict.Add("test", "value");
            MockSerializable nested = new MockSerializable(32, "testNested");

            MockSerializable2 obj = new MockSerializable2(5, "test", stringList, dict, nested);
            StorageToken token = obj.saveToToken();
            MockSerializable2 copy = (MockSerializable2)SuperGLU_Serializable.createFromToken(token);

            Assert.AreEqual(obj, copy);
        }


        [TestMethod()]
        public void testSerializeObject()
        {
            List<String> stringList = new List<string>();
            stringList.Add("Penguins");
            stringList.Add("birds");

            Dictionary<String, String> dict = new Dictionary<string, string>();
            dict.Add("test", "value");
            MockSerializable nested = new MockSerializable(32, "testNested");

            MockSerializable2 obj = new MockSerializable2(5, "test", stringList, dict, nested);

            string json = SerializationConvenience.serializeObject(obj, SerializationFormatEnum.JSON_FORMAT);

            Console.WriteLine(json);
        }

    }
}