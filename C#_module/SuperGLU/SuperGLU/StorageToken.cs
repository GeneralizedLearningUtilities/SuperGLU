using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SuperGLU
{
    public class StorageToken
    {
        private static String ID_KEY = "id";
        private static String CLASS_ID_KEY = "classId";

        private static HashSet<String> reservedKeys = new HashSet<String>();

        public Dictionary<String, Object> data
        { get; set; }

        static StorageToken()
        {
            reservedKeys.Add(ID_KEY);
            reservedKeys.Add(CLASS_ID_KEY);
        }


        public StorageToken()
        {
            this.data = new Dictionary<string, object>();
        }


        public StorageToken(Dictionary<String, Object> data, String id, String classId)
        {
            this.data = data;
            if (data == null)
                data = new Dictionary<string, object>();

            if (id != null)
            {
                this.setId(id);
            }
            else if (!this.data.Keys.Contains(ID_KEY))
            {
                this.data.Add(ID_KEY, System.Guid.NewGuid().ToString());
            }

            if (classId != null)
            {
                this.setClassId(classId);
            }


        }

        public String getId()
        {
            return (String)this.data[ID_KEY];
        }

        public void setId(String id)
        {
            this.data[ID_KEY] = id;
        }

        public String getClassId()
        {
            return (String)this.data[CLASS_ID_KEY];
        }

        public void setClassId(String classId)
        {
            this.data[CLASS_ID_KEY] = classId;
        }

        public int getSize()
        {
            return data.Count;
        }

        public bool contains(String key)
        {
            return this.data.ContainsKey(key);
        }

        public Object getItem(String key, bool hasDefault, Object defalt)
        {


            if (hasDefault)
                if (this.data.ContainsKey(key))
                    return this.data[key];
                else
                    return defalt;
            else
                return this.data[key];
        }

        public void setItem(String key, Object value)
        {
            this.data[key] = value;
        }

        public void removeItem(String key)
        {
            this.data.Remove(key);
        }

        public Object getItem(String key)
        {
            return this.getItem(key, false, null);
        }
    }
 }