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
      private MessagingGateway gateway;
      private string userId;
      private string classroomId;
      private string taskId;
      private string url;
      private ActivityType activityType;
      private Context context;
      private string serviceId;
      private DateTime startTime;

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
    }
}
