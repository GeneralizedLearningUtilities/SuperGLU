/** SuperGLU (Generalized Learning Utilities) Standard API
 This manages all versioning within the core libraries.

 Package: SuperGLU (Generalized Learning Utilities)
 Author: Benjamin Nye
 License: APL 2.0
 **/
const Zet = require('./util/zet')
    , Serialization = require('./util/serialization')
    , Message = require('./core/message')
    , Messaging = require('./core/messaging')
    , Messaging_Gateway = require('./core/messaging-gateway')
    , ReferenceData = require('./reference-data')
    , Heartbeat_Service = require('./services/orchestration/heartbeat-service')
    , StandardITSLoggingService = require('./services/logging/standard-its-logging')
    , LearningTask = require('./services/studentmodel/learning-task')
    , SerializableAssistmentsItem = require('./services/studentmodel/serializable-assistments-item')
    , UserDataServiceInterface = require('./services/authentication/User_Service_Client')
    , LocalStorageService = require('./services/storage/local-storage-service')
    , StorageServiceInterface = require('./services/storage/storage-service-client')

window.ReferenceData = ReferenceData
var namespace = window.SuperGLU = window.SuperGLU || {}
namespace.version = "0.1.9"

// Core API Modules
namespace.Zet = window.Zet = Zet
namespace.Serialization = Serialization
namespace.Messaging = Messaging
namespace.Messaging.Message = Message
namespace.Messaging_Gateway = Messaging_Gateway
namespace.VERBS = {}
namespace.CONTEXT_KEYS = {}
namespace.ReferenceData = ReferenceData
// Services
namespace.Heartbeat_Service = Heartbeat_Service
namespace.StandardITSLoggingService = StandardITSLoggingService
namespace.LearningTask = LearningTask
namespace.SerializableAssistmentsItem = SerializableAssistmentsItem
namespace.User_Service_Client = {UserDataServiceInterface: UserDataServiceInterface}
namespace.LocalStorageService = LocalStorageService
namespace.StorageServiceInterface = StorageServiceInterface

module.exports = namespace