using Microsoft.VisualStudio.TestTools.UnitTesting;
using SuperGLU;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SuperGLU.Tests
{
    [TestClass()]
    public class TokenRWFormatTests
    {
        [TestMethod()]
        public void SerializeTest()
        {
            Dictionary<String, Object> data = new Dictionary<string, object>();

            StorageToken token = new StorageToken(data, "id", "classID");
            List<String> stringlist = new List<string>();
            stringlist.Add("test1");
            stringlist.Add("test2");

            token.setItem("stringList", stringlist);

            Dictionary<String, String> stringMap = new Dictionary<string, string>();
            stringMap.Add("penguin", "penguin");

            token.setItem("stringMap", stringMap);

            object result = JSONStandardRWFormat.serialize(token); 

        }


        [TestMethod()]
        public void parseTest()
        {
            Dictionary<String, Object> data = new Dictionary<string, object>();

            StorageToken token = new StorageToken(data, "id", "classID");
            List<String> stringlist = new List<string>();
            stringlist.Add("test1");
            stringlist.Add("test2");

            token.setItem("stringList", stringlist);

            Dictionary<String, String> stringMap = new Dictionary<string, string>();
            stringMap.Add("penguin", "penguin");

            token.setItem("stringMap", stringMap);

            String result = JSONStandardRWFormat.serialize(token);

            StorageToken copy = JSONStandardRWFormat.parse(result);
        }


        [TestMethod()]
        public void serializeSuperGLUTest()
        {
            Dictionary<String, Object> data = new Dictionary<string, object>();

            StorageToken token = new StorageToken(data, "id", "classID");
            List<String> stringlist = new List<string>();
            stringlist.Add("test1");
            stringlist.Add("test2");

            token.setItem("stringList", stringlist);

            Dictionary<String, String> stringMap = new Dictionary<string, string>();
            stringMap.Add("penguin", "penguin");

            token.setItem("stringMap", stringMap);

            object result = JSONRWFormat.serialize(token);
        }


        [TestMethod()]
        public void parseSuperGLUTest()
        {
            Dictionary<String, Object> data = new Dictionary<string, object>();

            StorageToken nestedToken = new StorageToken(new Dictionary<string, object>(), "nested", "nestedClass");

            StorageToken token = new StorageToken(data, "id", "classID");
            List<String> stringlist = new List<string>();
            stringlist.Add("test1");
            stringlist.Add("test2");

            token.setItem("stringList", stringlist);

            Dictionary<String, String> stringMap = new Dictionary<string, string>();
            stringMap.Add("penguin", "penguin");

            token.setItem("stringMap", stringMap);

            token.setItem("nestedToken", nestedToken);

            string result = JSONRWFormat.serialize(token);
            StorageToken copy = JSONRWFormat.parse(result);
        }
    }
}