using System;
using System.Collections.Generic;
using System.Collections;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SuperGLU
{
    public class SuperGLU_Serializable
    {
        protected String id;


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
            return this.GetType().AssemblyQualifiedName;
        }


        public virtual void initializeFromToken(StorageToken token)
        {
            this.id = token.getId();
        }


        public virtual StorageToken saveToToken()
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
            clazz = Type.GetType(classId);

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

    public enum SerializationFormatEnum
    {
        JSON_FORMAT,
        JSON_STANDARD_FORMAT
    }


    public class SerializationConvenience
    {
        public static String makeSerialized(StorageToken token, SerializationFormatEnum sFormat)
        {
            if (sFormat == SerializationFormatEnum.JSON_FORMAT)
                return JSONRWFormat.serialize(token);

            else if (sFormat == SerializationFormatEnum.JSON_STANDARD_FORMAT)
                return JSONStandardRWFormat.serialize(token);

            throw new Exception("invalid format exception:" + sFormat);
        }


        public static StorageToken makeNative(String input, SerializationFormatEnum sFormat)
        {
            if (sFormat == SerializationFormatEnum.JSON_FORMAT)
                return JSONRWFormat.parse(input);

            else if (sFormat == SerializationFormatEnum.JSON_STANDARD_FORMAT)
                return JSONStandardRWFormat.parse(input);

            throw new Exception("invalid format exception:" + sFormat);
        }


        public static Object tokenizeObject(Object obj)
        {
            if (obj == null)
                return null;

            else if (obj.GetType().IsAssignableFrom(typeof(SuperGLU_Serializable)))
                return ((SuperGLU_Serializable)obj).saveToToken();

            else if (obj.GetType().IsGenericType)
            {
                Type genericType = obj.GetType().GetGenericTypeDefinition();

                if (TokenRWFormat.VALID_SEQUENCE_TYPES.Contains(genericType))
                {
                    List<Object> result = new List<object>();
                    dynamic objAsDynamic = (dynamic)obj;

                    foreach (Object child in objAsDynamic)
                    {
                        result.Add(tokenizeObject(child));
                    }
                    return result;

                }
                else if (TokenRWFormat.VALID_MAPPING_TYPES.Contains(genericType))
                {
                    Dictionary<Object, Object> result = new Dictionary<object, object>();

                    dynamic objAsDynamic = (dynamic)obj;

                    foreach (KeyValuePair<object, object> entry in objAsDynamic)
                    {
                        result.Add(tokenizeObject(entry.Key), tokenizeObject(entry.Value));
                    }
                    return result;
                }
                throw new Exception("unknown generic type for object : " + obj.ToString());
            }
            else
                return obj;
        }


        public static Object untokenizeObject(Object obj)
        {
            if (obj == null)
                return null;

            if (obj.GetType().IsAssignableFrom(typeof(StorageToken)))
                return SuperGLU_Serializable.createFromToken((StorageToken)obj);

            else if (obj.GetType().IsGenericType)
            {
                if (TokenRWFormat.VALID_SEQUENCE_TYPES.Contains(obj.GetType().GetGenericTypeDefinition()))
                {
                    List<Object> result = new List<object>();

                    IEnumerable dataEnumurator = (IEnumerable)obj;
                    foreach (Object o in dataEnumurator)
                    {
                        result.Add(untokenizeObject(o));
                    }

                    return result;
                }
                else if (TokenRWFormat.VALID_MAPPING_TYPES.Contains(obj.GetType().GetGenericTypeDefinition()))
                {
                    Dictionary<Object, Object> result = new Dictionary<object, object>();

                    dynamic objAsDynamic = (dynamic)obj;

                    foreach (KeyValuePair<object, object> entry in objAsDynamic)
                    {
                        result.Add(untokenizeObject(entry.Key), untokenizeObject(entry.Value));
                    }
                    return result;
                }
                else
                {
                    throw new Exception("unknown generic type for object : " + obj.ToString());
                }
            }
            else
                return obj;
        }
    }
}
