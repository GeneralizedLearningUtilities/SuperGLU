using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace SuperGLU
{
    public class TokenRWFormat
    {
        protected static List<Type> VALID_KEY_TYPES = new List<Type>();
        protected static List<Type> VALID_SEQUENCE_TYPES = new List<Type>();
        protected static List<Type> VALID_ATOMIC_VALUE_TYPES = new List<Type>();
        protected static List<Type> VALID_MAPPING_TYPES = new List<Type>();

        protected static List<Type> VALID_VALUE_TYPES = new List<Type>();
         

        static TokenRWFormat()
        {
            VALID_KEY_TYPES.Add(typeof(String));

            VALID_ATOMIC_VALUE_TYPES.Add(typeof(bool));
            VALID_ATOMIC_VALUE_TYPES.Add(typeof(int));
            VALID_ATOMIC_VALUE_TYPES.Add(typeof(float));
            VALID_ATOMIC_VALUE_TYPES.Add(typeof(String));

            VALID_SEQUENCE_TYPES.Add(typeof(List<>));

            VALID_MAPPING_TYPES.Add(typeof(Dictionary<,>));
        }


        //public static Object parse
     
    }
}
