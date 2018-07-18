using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SuperGLU {
    public class BaseLearnLogger: BaseService {   // BaseService not implemented

      /* Member variables

      Arguments:
      gateway -- the parent getway for this service (not implemented)
      userId -- unique id for the user
      classroomId -- unique id for the classroom cohort (optional), `null` if classroomId not specified
      taskId -- uuid string
      url -- the current base URL for the task that is being performed. This should not include situational parameters such as userId
      activityType -- the type of activity. This should be a unique system UUID (e.g. "AutoTutor_asdf2332gsa" or "www.autotutor.com/asdf2332gsa")
                       This ID should be the same for all activities presented by this system, since it will be used to query their results.
      context -- 'registration' property, which is essentially xAPI's concept of session id.
      serviceId -- the uuid for this service. Use random uuid if not specified.
      startTime -- time of starting the logging service
      */
      private MessagingGateway? gateway;
      private string? userId;
      private string? classroomId;
      private string? taskId;
      private string? url;
      private ActivityType? activityType;
      private Dictionary? context;
      private string? serviceId;
      private DateTime? startTime;

      // Constructor
      public BaseLearnLogger(MessagingGateway gateway, string userId, string name, string classroomId, string taskId, string url, ActivityType activityType, Context context, string serviceId) : base() {
        gateway = gateway;
        userId = userId;
        name = name;
        classroomId = classroomId;
        taskId = taskId;
        url = url;
        activityType = activityType;
        context = context;
        serviceId = serviceId;
        startTime = DateTime.Now;
      }

      // Calculate the duration so far (in seconds)
      // TODO: Perhaps this should be done automatically once a completed or terminated message arrives.
      public DateTime CalculateDuration(DateTime startTime=null, DateTime endTime=null) {
         DateTime startTime = startTime ?? this.startTime;
         DateTime endTime = endTime ?? DateTime.Now;
         DateTime duration = (endTime - starTime)/1000.0;
         if (duration < 0) {
           Console.WriteLine("Warning: Calculated duration less than zero.");
         }
         return duration;
      }

      // Perhaps this should be done automatically once startTask is called. Similarly for Lesson, Sublesson.
      public void SetTaskId(string taskId) {
        this.taskId = taskId;
      }

      public void GetTaskId() {
        return this.taskId;
      }

      // TO-DO: May need something like generic dictionary??
      public void SetContextValue(string key, <generic> value) {
        // TO-DO
      }

      // TODO: what is the return type? (because of the generic dictionary)
      public void GetContextValue(string key) {
        <generic> result;
        return this.context.TryGetValue(key, out result);
      }

      public bool HasContextValue(string key) {
        return this.context.ContainsKey(key);
      }

      public Message AddContextToMessage(Message msg, Dictionary context) {
        // TO-DO
      }

      // Finalize any post-processing of the message and write message to a json file
      // TO-DO: how to get verb and obj information??
      //        SendMessage method not implemented
      public void SendLoggingMessage(Message msg, Dictionary context=null) {
        msg = this.AddContextToMessage(msg, context);
        this.SendMessage(msg);
      }

      // TO-DO: Define what message to send (same for the rest of sending methods)
      public void SendStartSession(){
        Message msg = Message();
        this.SendLoggingMessage(msg);
      }
      
    }
}
