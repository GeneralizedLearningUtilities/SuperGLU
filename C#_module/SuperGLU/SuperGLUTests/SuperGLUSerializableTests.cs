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
    public class SuperGLUSerializableTests
    {
        [TestMethod()]
        public void CloneTest()
        {
            SuperGLU_Serializable original = new SuperGLU_Serializable("test");
            SuperGLU_Serializable clone = original.clone(false);
            Assert.AreEqual(original, clone);
        }

    }
}