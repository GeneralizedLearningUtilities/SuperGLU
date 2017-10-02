package edu.usc.ict.superglu.ontology.mappings;

import edu.usc.ict.superglu.core.GIFTMessage;
import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.core.VHMessage;
import edu.usc.ict.superglu.ontology.converters.*;
import edu.usc.ict.superglu.util.Pair;
import edu.usc.ict.superglu.util.StorageToken;
import edu.usc.ict.superglu.vhuman.GIFTVHumanBridge;

import java.net.InetAddress;
import java.net.UnknownHostException;
import java.util.*;

/**
 * This class is intended as a stopgap measure to build the mappings in the Java
 * code. It will be replaced once we implement the code to generate the
 * Mappings' JSON.
 *
 * @author auerbach
 */
public class MessageMapFactory {


    private static String NO_TEXT = "no text available";


    protected static MessageTemplate buildGenericGIFTMessage() throws UnknownHostException {

        List<Pair<FieldData, Object>> templateData = new ArrayList<>();

        List<Pair<Class<?>, String>> senderModuleTypePath = new ArrayList<>();
        senderModuleTypePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        senderModuleTypePath.add(new Pair<Class<?>, String>(String.class, "SenderModuleType"));
        FieldData senderModuleType = new NestedAtomic(senderModuleTypePath);

        templateData.add(new Pair<FieldData, Object>(senderModuleType, "VHMSGBridge_Module"));

        List<Pair<Class<?>, String>> senderQueueNamePath = new ArrayList<>();
        senderQueueNamePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        senderQueueNamePath.add(new Pair<Class<?>, String>(String.class, "SenderQueueName"));
        FieldData senderQueueName = new NestedAtomic(senderQueueNamePath);

        templateData.add(new Pair<FieldData, Object>(senderQueueName, "VHMSG_QUEUE:" + InetAddress.getLocalHost().getHostAddress() + ":Inbox"));

        List<Pair<Class<?>, String>> needsACKPath = new ArrayList<>();
        needsACKPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        needsACKPath.add(new Pair<Class<?>, String>(String.class, "NeedsACK"));
        FieldData needsACK = new NestedAtomic(needsACKPath);

        templateData.add(new Pair<FieldData, Object>(needsACK, false));


        List<Pair<Class<?>, String>> timestampPath = new ArrayList<>();
        timestampPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        timestampPath.add(new Pair<Class<?>, String>(String.class, "Time_Stamp"));
        FieldData timeStamp = new NestedAtomic(timestampPath);

        templateData.add(new Pair<FieldData, Object>(timeStamp, 0));

        List<Pair<Class<?>, String>> sequenceNumberPath = new ArrayList<>();
        sequenceNumberPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        sequenceNumberPath.add(new Pair<Class<?>, String>(String.class, "SequenceNumber"));
        FieldData sequenceNumber = new NestedAtomic(sequenceNumberPath);

        templateData.add(new Pair<FieldData, Object>(sequenceNumber, 0));

        List<Pair<Class<?>, String>> senderModuleNamePath = new ArrayList<>();
        senderModuleNamePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        senderModuleNamePath.add(new Pair<Class<?>, String>(String.class, "SenderModuleName"));
        FieldData senderModuleName = new NestedAtomic(senderModuleNamePath);

        templateData.add(new Pair<FieldData, Object>(senderModuleName, "VHMSGBridge_Module"));

        MessageTemplate result = new MessageTemplate(templateData);

        return result;
    }

    protected static MessageTemplate buildGIFTDomainSessionMessageTemplate() throws UnknownHostException {
        MessageTemplate result = buildGenericGIFTMessage();

        List<Pair<FieldData, Object>> templateData = result.getDefaultFieldData();
        List<Pair<Class<?>, String>> dsIDPath = new ArrayList<>();
        dsIDPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        dsIDPath.add(new Pair<Class<?>, String>(String.class, "SessionId"));
        FieldData dsId = new NestedAtomic(dsIDPath);

        templateData.add(new Pair<FieldData, Object>(dsId, GIFTVHumanBridge.GIFT_DOMAIN_SESSION_ID_KEY));

        List<Pair<Class<?>, String>> userIDPath = new ArrayList<>();
        userIDPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        userIDPath.add(new Pair<Class<?>, String>(String.class, "UserId"));
        FieldData userId = new NestedAtomic(userIDPath);

        templateData.add(new Pair<FieldData, Object>(userId, GIFTVHumanBridge.GIFT_USER_ID_KEY));

        List<Pair<Class<?>, String>> userNamePath = new ArrayList<>();
        userNamePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        userNamePath.add(new Pair<Class<?>, String>(String.class, "userName"));
        FieldData userName = new NestedAtomic(userNamePath);

        templateData.add(new Pair<FieldData, Object>(userName, GIFTVHumanBridge.GIFT_USER_NAME_KEY));

        return result;
    }


    protected static void buildConceptAssessmentTemplateData(List<Pair<FieldData, Object>> templateData) {
        List<Pair<Class<?>, String>> namePath = new ArrayList<>();
        namePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        namePath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        namePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        namePath.add(new Pair<Class<?>, String>(ArrayList.class, "concepts"));
        namePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        namePath.add(new Pair<Class<?>, String>(String.class, "name"));

        FieldData name = new NestedAtomic(namePath);
        templateData.add(new Pair<>(name, "KC"));


        List<Pair<Class<?>, String>> assessmentPath = new ArrayList<>();
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        assessmentPath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentPath.add(new Pair<Class<?>, String>(ArrayList.class, "concepts"));
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentPath.add(new Pair<Class<?>, String>(String.class, "assessment"));

        FieldData assessment = new NestedAtomic(assessmentPath);
        templateData.add(new Pair<>(assessment, "Unknown"));

        List<Pair<Class<?>, String>> timePath = new ArrayList<>();
        timePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        timePath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        timePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        timePath.add(new Pair<Class<?>, String>(ArrayList.class, "concepts"));
        timePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        timePath.add(new Pair<Class<?>, String>(long.class, "time"));

        FieldData time = new NestedAtomic(timePath);
        templateData.add(new Pair<>(time, ""));


        List<Pair<Class<?>, String>> idPath = new ArrayList<>();
        idPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        idPath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        idPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        idPath.add(new Pair<Class<?>, String>(ArrayList.class, "concepts"));
        idPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        idPath.add(new Pair<Class<?>, String>(Integer.class, "id"));

        FieldData id = new NestedAtomic(idPath);
        templateData.add(new Pair<>(id, new Random().nextInt(Integer.MAX_VALUE)));

        List<Pair<Class<?>, String>> clazzPath2 = new ArrayList<>();
        clazzPath2.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        clazzPath2.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        clazzPath2.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        clazzPath2.add(new Pair<Class<?>, String>(ArrayList.class, "concepts"));
        clazzPath2.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        clazzPath2.add(new Pair<Class<?>, String>(Integer.class, "assessmentType"));

        FieldData clazz2 = new NestedAtomic(clazzPath2);
        templateData.add(new Pair<>(clazz2, "mil.arl.gift.common.ConceptAssessment"));
    }


    protected static MessageTemplate buildPerformanceAssessmentMessageTemplate() throws UnknownHostException {
        MessageTemplate result = buildGIFTDomainSessionMessageTemplate();

        List<Pair<FieldData, Object>> templateData = result.getDefaultFieldData();

        List<Pair<Class<?>, String>> namePath = new ArrayList<>();
        namePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        namePath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        namePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        namePath.add(new Pair<Class<?>, String>(String.class, "name"));

        FieldData name = new NestedAtomic(namePath);
        templateData.add(new Pair<>(name, "KC"));


        List<Pair<Class<?>, String>> assessmentPath = new ArrayList<>();
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        assessmentPath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentPath.add(new Pair<Class<?>, String>(String.class, "assessment"));

        FieldData assessment = new NestedAtomic(assessmentPath);
        templateData.add(new Pair<>(assessment, "Unknown"));

        List<Pair<Class<?>, String>> timePath = new ArrayList<>();
        timePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        timePath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        timePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        timePath.add(new Pair<Class<?>, String>(long.class, "time"));

        FieldData time = new NestedAtomic(timePath);
        templateData.add(new Pair<>(time, ""));


        List<Pair<Class<?>, String>> idPath = new ArrayList<>();
        idPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        idPath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        idPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        idPath.add(new Pair<Class<?>, String>(Integer.class, "id"));

        FieldData id = new NestedAtomic(idPath);
        templateData.add(new Pair<>(id, new Random().nextInt(Integer.MAX_VALUE)));

        List<Pair<Class<?>, String>> clazzPath2 = new ArrayList<>();
        clazzPath2.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        clazzPath2.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        clazzPath2.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        clazzPath2.add(new Pair<Class<?>, String>(Integer.class, "assessmentType"));

        FieldData clazz2 = new NestedAtomic(clazzPath2);
        templateData.add(new Pair<>(clazz2, "mil.arl.gift.common.TaskAssessment"));

        List<Pair<Class<?>, String>> messageTypePath = new ArrayList<>();
        messageTypePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        messageTypePath.add(new Pair<Class<?>, String>(String.class, "Message_Type"));
        FieldData messageType = new NestedAtomic(messageTypePath);

        templateData.add(new Pair<FieldData, Object>(messageType, "PerformanceAssessment"));

        List<Pair<Class<?>, String>> destinationQueueNamePath = new ArrayList<>();
        destinationQueueNamePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        destinationQueueNamePath.add(new Pair<Class<?>, String>(String.class, "DestinationQueueName"));
        FieldData destinationQueueName = new NestedAtomic(destinationQueueNamePath);

        templateData.add(new Pair<FieldData, Object>(destinationQueueName, "Learner_Queue:" + InetAddress.getLocalHost().getHostAddress() + ":Inbox"));

        buildConceptAssessmentTemplateData(templateData);

        return result;
    }


    protected static MessageTemplate buildLessonCompleteMessageTemplate() throws UnknownHostException {
        MessageTemplate result = buildGIFTDomainSessionMessageTemplate();
        List<Pair<FieldData, Object>> templateData = result.getDefaultFieldData();

        List<Pair<Class<?>, String>> messageTypePath = new ArrayList<>();
        messageTypePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        messageTypePath.add(new Pair<Class<?>, String>(String.class, "Message_Type"));
        FieldData messageType = new NestedAtomic(messageTypePath);

        templateData.add(new Pair<FieldData, Object>(messageType, "LessonCompleted"));
        List<Pair<Class<?>, String>> destinationQueueNamePath = new ArrayList<>();
        destinationQueueNamePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        destinationQueueNamePath.add(new Pair<Class<?>, String>(String.class, "DestinationQueueName"));
        FieldData destinationQueueName = new NestedAtomic(destinationQueueNamePath);

        templateData.add(new Pair<FieldData, Object>(destinationQueueName, "Pedagogical_Queue:" + InetAddress.getLocalHost().getHostAddress() + ":Inbox"));
        return result;
    }

    protected static MessageTemplate buildCompletedMessageTemplate() {
        List<Pair<FieldData, Object>> templateData = new ArrayList<>();

        SimpleFieldData verb = new SimpleFieldData(Message.VERB_KEY);
        templateData.add(new Pair<>(verb, "Completed"));
        MessageTemplate result = new MessageTemplate(templateData);

        return result;
    }


    protected static List<FieldMap> buildDomainSessionMappings() {
        List<FieldMap> result = new ArrayList<>();

        List<Pair<Class<?>, String>> dsIDPath = new ArrayList<>();
        dsIDPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        dsIDPath.add(new Pair<Class<?>, String>(String.class, "SessionId"));
        FieldData dsId = new NestedAtomic(dsIDPath);

        FieldMap domainSessionID = new FieldMapContextToOne(GIFTVHumanBridge.GIFT_DOMAIN_SESSION_ID_KEY, dsId);
        result.add(domainSessionID);

        List<Pair<Class<?>, String>> userIDPath = new ArrayList<>();
        userIDPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        userIDPath.add(new Pair<Class<?>, String>(String.class, "UserId"));
        FieldData userId = new NestedAtomic(userIDPath);

        FieldMap userIdMap = new FieldMapContextToOne(GIFTVHumanBridge.GIFT_USER_ID_KEY, userId);
        result.add(userIdMap);

        List<Pair<Class<?>, String>> userNamePath = new ArrayList<>();
        userNamePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        userNamePath.add(new Pair<Class<?>, String>(String.class, "userName"));
        FieldData userName = new NestedAtomic(userNamePath);

        FieldMap userNameMap = new FieldMapContextToOne(GIFTVHumanBridge.GIFT_USER_NAME_KEY, userName);
        result.add(userNameMap);


        List<Pair<Class<?>, String>> timestampPath = new ArrayList<>();
        timestampPath.add(new Pair<Class<?>, String>(String.class, Message.TIMESTAMP_KEY));
        FieldData timestamp = new SimpleFieldData(Message.TIMESTAMP_KEY);

        List<Pair<Class<?>, String>> outTimestampPath = new ArrayList<>();
        outTimestampPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        outTimestampPath.add(new Pair<Class<?>, String>(String.class, "Time_Stamp"));
        FieldData outTimestamp = new NestedSubAtomic(outTimestampPath, new TimestampStringToLong(), new TimestampLongToString());

        FieldMap timestampMap = new FieldMapOneToOne(timestamp, outTimestamp);
        result.add(timestampMap);

        return result;
    }


    protected static List<FieldMap> buildCompletedtoPerformanceAssessmentsMappings() {
        List<FieldMap> result = buildDomainSessionMappings();


        SimpleFieldData actor = new SimpleFieldData(Message.ACTOR_KEY);
        SimpleFieldData superGLUResultField = new SimpleFieldData(Message.RESULT_KEY);
        FieldData timestamp = new SimpleFieldData(Message.TIMESTAMP_KEY);

        List<Pair<Class<?>, String>> timestampPath = new ArrayList<>();
        timestampPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        timestampPath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        timestampPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        timestampPath.add(new Pair<Class<?>, String>(long.class, "time"));

        FieldData giftTimestamp = new NestedSubAtomic(timestampPath, new TimestampStringToLong(), new TimestampLongToString());

        FieldMap timestampToGIFTTimestamp = new FieldMapOneToOne(timestamp, giftTimestamp);

        result.add(timestampToGIFTTimestamp);

        List<Pair<Class<?>, String>> assessmentPath = new ArrayList<>();
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        assessmentPath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentPath.add(new Pair<Class<?>, String>(String.class, "assessment"));

        List<String> assesmentLevelEnumValues = new ArrayList<>();
        assesmentLevelEnumValues.add("BelowExpectation");
        assesmentLevelEnumValues.add("AtExpectation");
        assesmentLevelEnumValues.add("AboveExpectation");

        FieldData assessment = new NestedSubAtomic(assessmentPath, new FloatToEnum(assesmentLevelEnumValues, 0.0f, 100.0f), new DummyConverter());
        FieldMap resultToShortTermMap = new FieldMapOneToOne(superGLUResultField, assessment);
        result.add(resultToShortTermMap);

        List<Pair<Class<?>, String>> assessmentNamePath = new ArrayList<>();
        assessmentNamePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        assessmentNamePath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        assessmentNamePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentNamePath.add(new Pair<Class<?>, String>(String.class, "name"));

        FieldData assessmentName = new NestedAtomic(assessmentNamePath);
        FieldMap objectToAssessmentName = new FieldMapOneToOne(actor, assessmentName);
        result.add(objectToAssessmentName);

        buildConceptAssessmentMappings(result);

        return result;
    }


    private static void buildConceptAssessmentMappings(List<FieldMap> result) {
        SimpleFieldData object = new SimpleFieldData(Message.OBJECT_KEY);
        SimpleFieldData actor = new SimpleFieldData(Message.ACTOR_KEY);
        SimpleFieldData superGLUResultField = new SimpleFieldData(Message.RESULT_KEY);
        FieldData timestamp = new SimpleFieldData(Message.TIMESTAMP_KEY);

        List<Pair<Class<?>, String>> timestampPath = new ArrayList<>();
        timestampPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        timestampPath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        timestampPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        timestampPath.add(new Pair<Class<?>, String>(ArrayList.class, "concepts"));
        timestampPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        timestampPath.add(new Pair<Class<?>, String>(long.class, "time"));

        FieldData giftTimestamp = new NestedSubAtomic(timestampPath, new TimestampStringToLong(), new TimestampLongToString());

        FieldMap timestampToGIFTTimestamp = new FieldMapOneToOne(timestamp, giftTimestamp);

        result.add(timestampToGIFTTimestamp);

        List<Pair<Class<?>, String>> assessmentPath = new ArrayList<>();
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        assessmentPath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentPath.add(new Pair<Class<?>, String>(ArrayList.class, "concepts"));
        assessmentPath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentPath.add(new Pair<Class<?>, String>(String.class, "assessment"));

        List<String> assesmentLevelEnumValues = new ArrayList<>();
        assesmentLevelEnumValues.add("BelowExpectation");
        assesmentLevelEnumValues.add("AtExpectation");
        assesmentLevelEnumValues.add("AboveExpectation");

        FieldData assessment = new NestedSubAtomic(assessmentPath, new FloatToEnum(assesmentLevelEnumValues, 0.0f, 100.0f), new DummyConverter());
        FieldMap resultToShortTermMap = new FieldMapOneToOne(superGLUResultField, assessment);
        result.add(resultToShortTermMap);

        List<Pair<Class<?>, String>> assessmentNamePath = new ArrayList<>();
        assessmentNamePath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        assessmentNamePath.add(new Pair<Class<?>, String>(ArrayList.class, "tasks"));
        assessmentNamePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentNamePath.add(new Pair<Class<?>, String>(ArrayList.class, "concepts"));
        assessmentNamePath.add(new Pair<Class<?>, String>(StorageToken.class, "0"));
        assessmentNamePath.add(new Pair<Class<?>, String>(String.class, "name"));

        FieldData assessmentName = new NestedAtomic(assessmentNamePath);
        FieldMap objectToAssessmentName = new FieldMapOneToOne(object, assessmentName);
        result.add(objectToAssessmentName);
    }


    protected static MessageMap buildCompletedToPerformanceAssessmentMapping() throws UnknownHostException {
        MessageType inMsg = new MessageType("Completed", 1.0f, 1.0f, buildCompletedMessageTemplate(),
                Message.class.getSimpleName());
        MessageType outMsg = new MessageType("PerformanceAssessment", 1.0f, 1.0f, buildPerformanceAssessmentMessageTemplate(),
                GIFTMessage.class.getSimpleName());
        MessageMap result = new MessageMap(inMsg, outMsg, buildCompletedtoPerformanceAssessmentsMappings());
        return result;
    }

    protected static DataConverter buildVRExpressStorageDataConverter(int index) {

        List<DataConverter> storageConverterList = new ArrayList<>();
        storageConverterList.add(new StringToList(" "));
        storageConverterList.add(new AddElementToStringList(index));
        storageConverterList.add(new ListToString(" "));
        DataConverter storageConverter = new CompoundConverter(storageConverterList);

        return storageConverter;
    }


    protected static DataConverter buildVRExpressRetrievalDataConverter(int index) {

        List<DataConverter> retrievalConverterList = new ArrayList<>();
        retrievalConverterList.add(new StringToList(" "));
        retrievalConverterList.add(new GetElementFromStringList(index));
        DataConverter retrievalConverter = new CompoundConverter(retrievalConverterList);

        return retrievalConverter;
    }


    protected static MessageTemplate buildGIFTDisplayFeedbackTutorRequestTemplate() {

        NestedAtomic header = new NestedAtomic(String.class, GIFTMessage.HEADER_KEY);
        List<Pair<FieldData, Object>> templateDataList = new ArrayList<>();
        templateDataList.add(new Pair<FieldData, Object>(header, "DisplayGuidanceTutorRequest"));

        List<Pair<Class<?>, String>> payloadPath = new ArrayList<>();

        payloadPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        payloadPath.add(new Pair<Class<?>, String>(String.class, "text"));

        NestedAtomic payload = new NestedAtomic(payloadPath);

        templateDataList.add(new Pair<FieldData, Object>(payload, NO_TEXT));

        MessageTemplate result = new MessageTemplate(templateDataList);

        return result;
    }


    protected static MessageTemplate buildSuperGLUGiveFeedbackMessageTemplate() {
        List<Pair<FieldData, Object>> templateDataList = new ArrayList<>();

        SimpleFieldData actor = new SimpleFieldData(Message.ACTOR_KEY);
        SimpleFieldData verb = new SimpleFieldData(Message.VERB_KEY);
        SimpleFieldData object = new SimpleFieldData(Message.OBJECT_KEY);
        SimpleFieldData result = new SimpleFieldData(Message.RESULT_KEY);


        templateDataList.add(new Pair<FieldData, Object>(actor, "GIFT"));
        templateDataList.add(new Pair<FieldData, Object>(verb, "GiveFeedback"));
        templateDataList.add(new Pair<FieldData, Object>(object, "VHuman"));
        templateDataList.add(new Pair<FieldData, Object>(result, NO_TEXT));


        MessageTemplate returnVal = new MessageTemplate(templateDataList);

        return returnVal;

    }


    protected static List<FieldMap> buildFieldMapsForDisplayFeedbackTutorRequestToGiveFeedback() {

        List<FieldMap> mappings = new ArrayList<>();

        List<Pair<Class<?>, String>> payloadPath = new ArrayList<>();

        payloadPath.add(new Pair<Class<?>, String>(StorageToken.class, GIFTMessage.PAYLOAD_KEY));
        payloadPath.add(new Pair<Class<?>, String>(String.class, "Text"));

        NestedAtomic payload = new NestedAtomic(payloadPath);

        List<Pair<Class<?>, String>> indices = new ArrayList<>();
        indices.add(new Pair<Class<?>, String>(String.class, Message.RESULT_KEY));
        //DataConverter converter = new XMLActWrapped("speech");
        //NestedSubAtomic result = new NestedSubAtomic(indices, build, 0);

        NestedAtomic result = new NestedAtomic(indices);

        FieldMapOneToOne map = new FieldMapOneToOne(payload, result);

        mappings.add(map);

        return mappings;
    }


    protected static MessageMap buildDisplayFeedbackTutorRequestToSuperGLU() {

        MessageType inMsgType = new MessageType("DisplayGuidanceTutorRequest", 1.0f, 1.0f, buildGIFTDisplayFeedbackTutorRequestTemplate(), GIFTMessage.class.getSimpleName());
        MessageType outMsgType = new MessageType("GiveFeedback", 1.0f, 1.0f, buildSuperGLUGiveFeedbackMessageTemplate(), Message.class.getSimpleName());
        MessageMap map = new MessageMap(inMsgType, outMsgType, buildFieldMapsForDisplayFeedbackTutorRequestToGiveFeedback());

        return map;
    }


    protected static MessageTemplate buildVRExpressTemplate() {

        List<Pair<Class<?>, String>> indices = new ArrayList<>();
        indices.add(new Pair<Class<?>, String>(String.class, VHMessage.BODY_KEY));

        NestedSubAtomic speaker = new NestedSubAtomic(indices, buildVRExpressStorageDataConverter(0), buildVRExpressRetrievalDataConverter(0));
        NestedSubAtomic audience = new NestedSubAtomic(indices, buildVRExpressStorageDataConverter(1), buildVRExpressRetrievalDataConverter(1));
        NestedSubAtomic number = new NestedSubAtomic(indices, buildVRExpressStorageDataConverter(2), buildVRExpressRetrievalDataConverter(2));

        List<DataConverter> storageConverterList = new ArrayList<>();
        storageConverterList.add(new XMLActWrapped("speech"));
        storageConverterList.add(buildVRExpressStorageDataConverter(3));

        DataConverter storageConverter = new CompoundConverter(storageConverterList);

        NestedSubAtomic utterance = new NestedSubAtomic(indices, storageConverter, buildVRExpressRetrievalDataConverter(3));

        List<Pair<FieldData, Object>> templateData = new ArrayList<>();
        templateData.add(new Pair<FieldData, Object>(speaker, "Rachel"));
        templateData.add(new Pair<FieldData, Object>(audience, "all"));
        templateData.add(new Pair<FieldData, Object>(number, "0"));
        templateData.add(new Pair<FieldData, Object>(utterance, "<speech></speech>"));

        templateData.add(new Pair<FieldData, Object>(new SimpleFieldData(VHMessage.FIRST_WORD_KEY), "vrExpress"));

        MessageTemplate template = new MessageTemplate(templateData);

        return template;
    }


    protected static FieldMap buildFieldMapForGiveFeedBackToVrExpress() {

        SimpleFieldData result = new SimpleFieldData(Message.RESULT_KEY);

        List<Pair<Class<?>, String>> indices = new ArrayList<>();
        indices.add(new Pair<Class<?>, String>(String.class, VHMessage.BODY_KEY));

        List<DataConverter> storageConverterList = new ArrayList<>();
        storageConverterList.add(new XMLActWrapped("speech"));
        storageConverterList.add(buildVRExpressStorageDataConverter(3));

        DataConverter storageConverter = new CompoundConverter(storageConverterList);

        NestedSubAtomic utterance = new NestedSubAtomic(indices, storageConverter, buildVRExpressRetrievalDataConverter(3));

        FieldMap returnVal = new FieldMapOneToOne(result, utterance);

        return returnVal;

    }


    protected static MessageMap buildGiveFeedBackToVHuman() {

        List<FieldMap> mappings = new ArrayList<>();
        mappings.add(buildFieldMapForGiveFeedBackToVrExpress());

        MessageType inMsg = new MessageType("GiveFeedback", 1.0f, 1.0f, buildSuperGLUGiveFeedbackMessageTemplate(), Message.class.getSimpleName());
        MessageType outMsg = new MessageType("vrExpress", 1.0f, 1.0f, buildVRExpressTemplate(), VHMessage.class.getSimpleName());

        MessageMap result = new MessageMap(inMsg, outMsg, mappings);

        return result;
    }


    public static Map<String, MessageTemplate> buildDefaultMessageTemplates() {

        Map<String, MessageTemplate> result = new HashMap<>();

        List<Pair<FieldData, Object>> vHumanTemplateData = new ArrayList<>();
        vHumanTemplateData.add(new Pair<FieldData, Object>(new SimpleFieldData(VHMessage.FIRST_WORD_KEY), ""));
        vHumanTemplateData.add(new Pair<FieldData, Object>(new SimpleFieldData(VHMessage.BODY_KEY), ""));
        MessageTemplate vhumanTemplate = new MessageTemplate(vHumanTemplateData);

        result.put(VHMessage.class.getSimpleName(), vhumanTemplate);


        List<Pair<FieldData, Object>> giftTemplateData = new ArrayList<>();
        giftTemplateData.add(new Pair<FieldData, Object>(new SimpleFieldData(GIFTMessage.HEADER_KEY), ""));
        giftTemplateData.add(new Pair<FieldData, Object>(new SimpleFieldData(GIFTMessage.PAYLOAD_KEY), ""));
        MessageTemplate giftTemplate = new MessageTemplate(giftTemplateData);

        result.put(GIFTMessage.class.getSimpleName(), giftTemplate);

        return result;
    }


    public static List<MessageMap> buildMessageMaps() {
        List<MessageMap> result = new ArrayList<>();
        result.add(buildDisplayFeedbackTutorRequestToSuperGLU());
        result.add(buildGiveFeedBackToVHuman());
        try {
            result.add(buildCompletedToPerformanceAssessmentMapping());
        } catch (UnknownHostException e) {
            e.printStackTrace();
        }

        return result;
    }
}
