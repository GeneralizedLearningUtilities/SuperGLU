﻿using Newtonsoft.Json.Linq;
using System;
using System.IO;
using System.Collections.Generic;
using TinCan;


namespace SuperGLU
{
    class xAPILearnLogger: BaseLearnLogger
    {
        string mbox = "mailto:SMART-E@ict.usc.edu";
        string activityURI = "http://id.tincanapi.com/activity/";

        /* ---------------- constructor, getter and setter --------------- */
        public xAPILearnLogger(string userId = "", string userName = ""): base()
        {
            this.userId = userId;
            this.userName = userName;
            this.url = new Uri("https://github.com/GeneralizedLearningUtilities/SuperGLU/");
        }

        public void SetUserId(string userId)
        {
            this.userId = userId;
        }

        public void SetUserName(string userName)
        {
            this.userName = userName;
        }

        /* ---------------------- create xAPI object ---------------------- */
        // create actor
        private Agent CreateActor(string name, string openid, string mbox)
        {
            Agent actor = new Agent();
            actor.name = name;
            actor.openid = openid;
            actor.mbox = mbox;

            return actor;
        }

        // create agent account, used as an instructor agent in context
        private AgentAccount CreateAgentAccount(string name, string homePage)
        {
            AgentAccount agentAccount = new AgentAccount();
            agentAccount.name = name;
            agentAccount.homePage = new Uri(homePage);

            return agentAccount;
        }

        // create verb
        private Verb CreateCompletedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/complete");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "completed");

            return verb;
        }

        private Verb CreateStartedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/start");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "started");

            return verb;
        }

        private Verb CreateTerminiatedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/terminate");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "terminated");

            return verb;
        }

        private Verb CreatePresentedVerb()
        {
            Verb verb = new Verb();
            verb.id = new Uri("http://activitystrea.ms/schema/1.0/present");
            verb.display = new LanguageMap();
            verb.display.Add("en-US", "presented");

            return verb;
        }

        // create activity
        private Activity CreateSession(string activityId, string name, string description)
        {
            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>(){ { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/tutor-session");

            return activity;
        }

        private Activity CreateTopic(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/topic");

            return activity;
        }

        private Activity CreateLesson(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/lesson");

            return activity;
        }

        private Activity CreateSublesson(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/sublesson");

            return activity;
        }

        private Activity CreateTask(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/task");

            return activity;
        }

        private Activity CreateStep(string activityId, string name, string description)
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/step");

            return activity;
        }

        private Activity CreateVideo(string activityId= "http://activitystrea.ms/schema/1.0/video", string name= "video", string description= "Video content of any kind")
        {

            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/video");

            return activity;
        }

        // TODO: activity tree class need to be implemented
        private Activity CreateActivityTree(string activityId = "http://activitystrea.ms/schema/1.0/activityTree", string name = "activityTree", string description = "Activity tree (not implemented yet)")
        {
            Activity activity = new Activity();
            activity.id = this.activityURI + activityId;
            activity.definition = new ActivityDefinition();
            activity.definition.name = new LanguageMap(new Dictionary<string, string>() { { "en-US", name } });
            activity.definition.description = new LanguageMap(new Dictionary<string, string>() { { "en-US", description } });
            activity.definition.type = new Uri("http://id.tincanapi.com/activitytype/activityTree");

            return activity;
        }

        // create result
        private Result CreateResult(string response = "", bool? success = null)
        {
            Result result = new Result();
            if (response != "")
            {
                result.response = response;
            }
            if (success != null)
            {
                result.success = success;
            }

            return result;
        }

        // create context
        private Context CreateContext(JObject contextJson)
        {   
            // instructor agent
            AgentAccount agentAccount = CreateAgentAccount("instructorAgent", "http://instructorHomepage.com");

            Context context = new Context();
            context.registration = Guid.NewGuid();   // globally unique indentifier
            context.instructor = new Agent(new JObject { { "account", agentAccount.ToJObject()} });
            context.extensions = new TinCan.Extensions(contextJson);    // 'Extensions' is ambiguous reference between 'Newtonsoft.Json' and 'TinCan'
            context.contextActivities = new ContextActivities();

            return context;
        }

        /* ------------------- construct xAPI statement ------------------- */
        // start
        public void SendStartSession(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateSession(activityId, name, description);
            Result result = CreateResult(response: "User started a new Session");
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendStartLesson(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateLesson(activityId, name, description);
            Result result = CreateResult(success: true);
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendStartSublesson(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateSublesson(activityId, name, description);
            Result result = CreateResult(success: true);
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendStartTask(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateTask(activityId, name, description);
            Result result = CreateResult(success: true);
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendStartStep(string activityId, string name, string description, JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateStartedVerb();
            Activity activity = CreateStep(activityId, name, description);
            Result result = CreateResult(success: true);
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        // terminiate or compplete
        public void SendTerminiatedSession(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateTerminiatedVerb();
            Activity activity = CreateActivityTree();   // activity tree class need to be implemented, this is a dummy method
            Result result = CreateResult();
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendCompletedLesson(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateCompletedVerb();
            Activity activity = CreateActivityTree();   // activity tree class need to be implemented, this is a dummy method
            Result result = CreateResult();
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendCompletedSublesson(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateCompletedVerb();
            Activity activity = CreateActivityTree();   // activity tree class need to be implemented, this is a dummy method
            Result result = CreateResult();
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        public void SendCompletedTask(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateCompletedVerb();
            Activity activity = CreateActivityTree();   // activity tree class need to be implemented, this is a dummy method
            Result result = CreateResult();
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        // TODO: work in progress
        public void SendCompletedStep(string choice, string customScoreURI, double customScore, JObject contextJson, double rawScore = -1, double maxScore = -1, double minScore = 0, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreateCompletedVerb();
            Activity activity = CreateActivityTree();
            Result result = new Result();
            Context context = CreateContext(contextJson);
            TinCan.Extensions extensions = new TinCan.Extensions(new JObject { {customScoreURI, customScore} });

            // handle different result
            if (rawScore != -1)
            {
                result.response = choice;
                result.score = new Score(new JObject { { "raw", rawScore }, { "min", minScore }, {"max", maxScore} });
                result.extensions = extensions;
            } else
            {
                result.response = choice;
                result.extensions = extensions;
            }

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }


        public void SendPresentedVideo(JObject contextJson, DateTime? timestamp = null)
        {
            Agent actor = CreateActor(this.userName, this.userId, this.mbox);
            Verb verb = CreatePresentedVerb();
            Activity activity = CreateVideo(); 
            Result result = CreateResult();
            Context context = CreateContext(contextJson);

            if (timestamp == null)
            {
                timestamp = GetTimeStamp();
            }

            JObject statementJson = new JObject
            {
                { "actor", actor.ToJObject() },
                { "verb", verb.ToJObject() },
                { "object", activity.ToJObject() },
                { "result", result.ToJObject() },
                { "context", context.ToJObject() },
                { "timestamp", timestamp }

            };

            Statement statement = new Statement(statementJson);
            this.SendLoggingMessage(statement);
        }

        private void SendLoggingMessage(Statement statement)
        {
            Console.WriteLine("{0}", statement.ToJSON());
            string path = Directory.GetCurrentDirectory();
            // write to log file
            using (System.IO.StreamWriter logFile =
                new System.IO.StreamWriter(path + "\\xAPILog.json", true))
                {
                    logFile.WriteLine(statement.ToJSON());
                }
        }
    }

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
            foreach (string line in batchData)
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


        public void ConvertToxAPI(Dictionary<string, string> data, xAPILearnLogger logger)
        {   
            Console.WriteLine(data["event"]);
            if (data["event"] == "StartSession")
            {
                logger.SendStartSession(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
            }
            else if (data["event"] == "StartVideoLesson")
            {
                logger.SendStartLesson(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
            }
            else if (data["event"] == "StartVideoSublesson")
            {
                logger.SendStartSublesson(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
            }
            else if (data["event"] == "StartScenario")
            {
                logger.SendStartStep(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
            }
            else if (data["event"] == "StartDialogue")
            {
                logger.SendPresentedVideo(new JObject { });
            }
            else if (data["event"] == "StartDecision")
            {
                logger.SendStartTask(data["activityId"], data["activityName"], data["activityDescription"], new JObject { });
            }
            else if (data["event"] == "TerminatedSession")
            {
                logger.SendTerminiatedSession(new JObject { });
            }
            else if (data["event"] == "CompletedVideoLesson")
            {
                logger.SendCompletedLesson(new JObject { });
            }
            else if (data["event"] == "CompletedVideoSublesson")
            {
                logger.SendCompletedSublesson(new JObject { });
            }
            else if (data["event"] == "CompletedScenario")
            {
                logger.SendCompletedStep("test choices", "http://custom_score_URI", 1, new JObject { });
            }
            else if (data["event"] == "SendCompletedDecision")
            {
                logger.SendCompletedTask(new JObject { });
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
            xAPILearnLogger logger = new xAPILearnLogger();

            loggerTester.ProcessBatchData(lines, logger);
            Console.ReadLine();
            
        }
    }


}
