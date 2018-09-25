using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SuperGLU
{
    public class SuperGLU_Serializable
    {
        protected String id;

        protected static Dictionary<String, Type> CLASS_IDS = new Dictionary<string, Type>();

        static SuperGLU_Serializable()
        {
            populateClassIds();
        }

        public static void populateClassIds()
        {
            foreach (var asm in AppDomain.CurrentDomain.GetAssemblies())
            {
                foreach (var type in asm.GetTypes())
                {
                    if (type.IsAssignableFrom( typeof(SuperGLU_Serializable)))
                        CLASS_IDS.Add(type.FullName, type);
                }
            }
        }


        public SuperGLU_Serializable(String id)
        {
            if (id == null)
                this.id = Guid.NewGuid().ToString();
            else
                this.id = id;
        }


        public SuperGLU_Serializable()
        {
            this.id = Guid.NewGuid().ToString();
        }


        protected Boolean fieldIsEqual(Object thisField, Object otherField)
        {
            if (thisField == null && otherField == null)
                return true;

            if (thisField == null)
                return false;

            if (otherField == null)
                return false;

            return thisField.Equals(otherField);
        }


        public override bool Equals(object otherObj)
        {
            if (otherObj == null)
                return false;

            if (!this.GetType().Equals(otherObj.GetType()))
                return false;

            SuperGLU_Serializable other = (SuperGLU_Serializable)otherObj;

            if (fieldIsEqual(this.id, other.id))
                return true;

            return false; 
        }


        public override int GetHashCode()
        {
            return this.id.GetHashCode();
        }

        
        public String getId()
        {
            return this.id;
        }


        public void updateId(String id)
        {
            if (id == null)
                this.id = Guid.NewGuid().ToString();
            else
                this.id = id;
        }


        public String getClassId()
        {
            return this.GetType().FullName;
        }


        public void initializeFromToken(StorageToken token)
        {
            this.id = token.getId();
        }


        public StorageToken saveToToken()
        {
            StorageToken token = new StorageToken(new Dictionary<string, object>(), this.id, this.getClassId());
            return token;
        }


        public SuperGLU_Serializable clone(bool newId)
        {
            StorageToken token = this.saveToToken();
            SuperGLU_Serializable copy = createFromToken(token);

            if (newId)
                copy.updateId(null);

            return copy;
        }


        public static SuperGLU_Serializable createFromToken(StorageToken token)
        {
            String classId = token.getClassId();

            Type clazz;
            if (CLASS_IDS.ContainsKey(classId))
                clazz = CLASS_IDS[classId];
            else
                clazz = null;

            if(clazz != null)
            { 
                SuperGLU_Serializable instance = (SuperGLU_Serializable)Activator.CreateInstance(clazz);
                instance.initializeFromToken(token);
                return instance;
                
            }

            //should never reach here
            return null;
        }
    }
}
