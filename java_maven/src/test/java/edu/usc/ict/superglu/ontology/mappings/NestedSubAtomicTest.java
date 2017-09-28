package edu.usc.ict.superglu.ontology.mappings;

import edu.usc.ict.superglu.ontology.converters.*;
import edu.usc.ict.superglu.util.Pair;
import edu.usc.ict.superglu.util.SerializationConvenience;
import edu.usc.ict.superglu.util.SerializationFormatEnum;
import edu.usc.ict.superglu.util.StorageToken;
import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

public class NestedSubAtomicTest {
    private NestedSubAtomic nestedSubAtomic;

    private StorageToken sampleData;

    @Before
    public void setUp() throws Exception {
        List<Pair<Class<?>, String>> indices = new ArrayList<>();
        indices.add(new Pair<Class<?>, String>(String.class, "foo"));

        List<DataConverter> storageConverterList = new ArrayList<>();
        storageConverterList.add(new StringToList(" "));
        storageConverterList.add(new AddElementToStringList(1));
        storageConverterList.add(new ListToString(" "));
        DataConverter storageConverter = new CompoundConverter(storageConverterList);

        List<DataConverter> retrievalConverterList = new ArrayList<>();
        retrievalConverterList.add(new StringToList(" "));
        retrievalConverterList.add(new GetElementFromStringList(1));
        DataConverter retrievalConverter = new CompoundConverter(retrievalConverterList);


        nestedSubAtomic = new NestedSubAtomic(indices, storageConverter, retrievalConverter);

        String foo = "test pass";
        sampleData = new StorageToken();
        sampleData.setItem("foo", foo);

    }

    @After
    public void tearDown() throws Exception {
        this.nestedSubAtomic = null;
        this.sampleData = null;
    }

    @Test
    public void testSaveToToken() {
        String serialized = SerializationConvenience.serializeObject(nestedSubAtomic, SerializationFormatEnum.JSON_FORMAT);
        NestedSubAtomic copy = (NestedSubAtomic) SerializationConvenience.nativeizeObject(serialized, SerializationFormatEnum.JSON_FORMAT);

        Assert.assertEquals(nestedSubAtomic, copy);
    }

    @Test
    public void testRetrieveFieldData() {
        String data = (String) nestedSubAtomic.retrieveFieldData(sampleData);
        Assert.assertEquals("pass", data);
    }

    @Test
    public void testStoreData() {
        StorageToken token = new StorageToken(new HashMap<>(), "testToken", "none");

        nestedSubAtomic.storeData(token, "pass");

        String result = (String) nestedSubAtomic.retrieveFieldData(token);

        Assert.assertEquals("pass", result);

    }


    @Test
    public void testOutOfOrderStorage() {
        List<Pair<Class<?>, String>> indices = new ArrayList<>();
        indices.add(new Pair<Class<?>, String>(String.class, "foo"));

        List<DataConverter> storageConverterList = new ArrayList<>();
        storageConverterList.add(new StringToList(" "));
        storageConverterList.add(new AddElementToStringList(0));
        storageConverterList.add(new ListToString(" "));
        DataConverter storageConverter = new CompoundConverter(storageConverterList);

        List<DataConverter> retrievalConverterList = new ArrayList<>();
        retrievalConverterList.add(new StringToList(" "));
        retrievalConverterList.add(new GetElementFromStringList(0));
        DataConverter retrievalConverter = new CompoundConverter(retrievalConverterList);


        NestedSubAtomic otherNestedSubAtomic = new NestedSubAtomic(indices, storageConverter, retrievalConverter);

        StorageToken token = new StorageToken(new HashMap<>(), "testToken", "none");

        nestedSubAtomic.storeData(token, "pass");
        otherNestedSubAtomic.storeData(token, "test");

        String firstResult = (String) nestedSubAtomic.retrieveFieldData(token);
        String secondResult = (String) otherNestedSubAtomic.retrieveFieldData(token);

        Assert.assertEquals("pass", firstResult);
        Assert.assertEquals("test", secondResult);
    }

}
