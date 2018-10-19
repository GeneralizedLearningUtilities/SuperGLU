using System;
using System.IO;
using TinCan;
using Microsoft.VisualStudio.TestTools.UnitTesting;

namespace SuperGLUTests
{
    [TestClass]
    public class ActivityTreeTest
    {
        [TestMethod]
        public void TestAddChild()
        {
            FileStream inFile = File.Open("../../Session.json", FileMode.Open);
            StreamReader reader = new StreamReader(inFile);
            string json = reader.ReadLine();
            Activity activity = new Activity(new TinCan.Json.StringOfJSON(json));

            FileStream inFile2 = File.Open("../../Video.json", FileMode.Open);
            StreamReader reader2 = new StreamReader(inFile);
            string json2 = reader.ReadLine();
            Activity activity2 = new Activity(new TinCan.Json.StringOfJSON(json));

            SuperGLU.ActivityTree tree = new SuperGLU.ActivityTree();
            tree.enterActivity(activity.id, activity, null);

            tree.enterActivity(activity.id, activity2, null);
            tree.exitActivity(null);
        }
    }
}
