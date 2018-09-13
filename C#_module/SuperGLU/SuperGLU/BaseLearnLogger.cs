using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using TinCan;

namespace SuperGLU
{
    public class BaseLearnLogger
    { 
        // construct properties
        protected string userId { get; set; }
        protected string userName { get; set; }
        protected string classRoomId { get; set; }
        protected string taskId { get; set; }
        protected Uri url { get; set; }
        protected string activityType { get; set; }
        protected IDictionary<string, string> context { get; set; }
        protected string anId { get; set; }

        public BaseLearnLogger() { }

        public DateTime GetTimeStamp()
        {
            return DateTime.Now;
        }
    }
}
