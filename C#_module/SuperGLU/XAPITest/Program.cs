using System;
using System.Collections.Generic;
using SuperGLU;
using Newtonsoft.Json.Linq;
using System.IO;
using TinCan;

// testing
class xAPILearnLoggerTester
{
    public string[] ReadFile(string file)
    {
        string[] lines = System.IO.File.ReadAllLines(file);

        return lines;
    }

    public void ProcessBatchData(string[] batchData, xAPILearnLogger logger)
    {
        bool firstLine = true;

        foreach (string line in batchData)
        {
            if (firstLine) { firstLine = false; }
            else
            {
                // split with tab delimiter
                string sep = "\t";
                string[] splitLine = line.Split(sep.ToCharArray());
                // store data in a dictionary
                Dictionary<string, string> data = new Dictionary<string, string>();
                data["event"] = splitLine[0];
                data["activityId"] = splitLine[1];
                data["activityName"] = splitLine[2];
                data["activityDescription"] = splitLine[3];

                ConvertToxAPI(data, logger);
            }
        }
    }


    public void ConvertToxAPI(Dictionary<string, string> data, xAPILearnLogger logger)
    {
        if (data["event"] == "StartSession")
        {
            logger.SendStartSession(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
        }
        else if ((data["event"] == "StartVideoLesson") || (data["event"] == "StartScenario"))
        {
            logger.SendStartLesson(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
        }
        else if ((data["event"] == "StartVideoSublesson") || (data["event"] == "StartAAR") || (data["event"] == "StartDialogue"))
        {
            logger.SendStartSublesson(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
        }
        else if ((data["event"] == "StartDecision") || (data["event"] == "StartQuestion"))
        {
            logger.SendStartTask(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
        }
        else if ((data["event"] == "StartChoice") || (data["event"] == "StartAnswer"))
        {
            logger.SendStartStep(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
        }
        else if (data["event"] == "TerminatedSession")
        {
            logger.SendTerminiatedSession(new JObject { });
        }
        else if ((data["event"] == "CompletedVideoLesson") || (data["event"] == "CompletedScenario"))
        {
            logger.SendCompletedLesson(new JObject { });
        }
        else if ((data["event"] == "CompletedVideoSublesson") || (data["event"] == "CompletedAAR") || (data["event"] == "CompletedDialogue"))
        {
            if (data["event"] == "CompletedDialogue")
            {
                logger.SendWatchedVideo(new JObject { });
            }
            logger.SendCompletedSublesson(new JObject { });
        }
        else if ((data["event"] == "CompletedDecision") || (data["event"] == "CompletedQuestion"))
        {
            logger.SendCompletedTask(new JObject { });
        }

        else if ((data["event"] == "CompletedChoice") || (data["event"] == "CompletedAnswer"))
        {
            logger.SendCompletedStep("test choices", "http://custom_score_URI", 1, new JObject { });
        }
        else
        {
            Console.WriteLine("Event not found: {0}", data["event"]);
        }
    }


    static void Main()
    {
        string path = Directory.GetCurrentDirectory();
        string file = path + "\\activity_data(975).txt";
        xAPILearnLoggerTester loggerTester = new xAPILearnLoggerTester();
        string[] lines = loggerTester.ReadFile(file);
        xAPILearnLogger logger = new xAPILearnLogger("testUserID", "testUserName");

        loggerTester.ProcessBatchData(lines, logger);
        Console.WriteLine("Press Enter to continue.");
        Console.ReadLine();
        Console.WriteLine("Exiting.");

    }
}
