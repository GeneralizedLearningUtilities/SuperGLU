package edu.usc.ict.superglu.util;

import edu.usc.ict.superglu.core.Message;
import edu.usc.ict.superglu.ontology.mappings.NestedAtomic;
import org.junit.Assert;
import org.junit.Test;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

public class SerializableTest {

    @Test
    public void testReflection() {
        SuperGlu_Serializable.populateClassIDs("edu.usc.ict.superglu");
    }


    @Test
    public void testSaveToStorageToken() {
        MockSerializables.MockSerializable ms = new MockSerializables.MockSerializable(-1, "penguins");
        ms.updateId("test1");
        StorageToken token = ms.saveToToken();
        System.out.println(token.toString());

        Assert.assertEquals("{\"MockSerializable\":{\"classId\":\"MockSerializable\",\"bar\":\"penguins\",\"foo\":-1,\"id\":\"test1\"}}", token.toString());
    }


    @Test
    public void testLoadFromStorageToken() {
        MockSerializables.MockSerializable ms = new MockSerializables.MockSerializable(-1, "penguins");
        StorageToken token = ms.saveToToken();
        MockSerializables.MockSerializable copy = (MockSerializables.MockSerializable) SuperGlu_Serializable.createFromToken(token);

        Assert.assertEquals(ms, copy);
    }


    @Test
    public void testSaveList() {
        List<String> testList = new ArrayList<>();
        testList.add("Emperor");
        testList.add("King");
        testList.add("Adelie");
        testList.add("Chinstrap");
        testList.add("Macaroni");
        testList.add("Gentoo");
        MockSerializables.MockSerializable2 ms2 = new MockSerializables.MockSerializable2(42, "penguins", testList);

        ms2.updateId("test2");

        StorageToken token = ms2.saveToToken();

        System.out.println(token.toString());
        Assert.assertEquals("{\"MockSerializable2\":{\"classId\":\"MockSerializable2\",\"bar\":\"penguins\",\"foo\":42,\"baz\":{\"list\":[\"Emperor\",\"King\",\"Adelie\",\"Chinstrap\",\"Macaroni\",\"Gentoo\"]},\"id\":\"test2\"}}", token.toString());
    }


    @Test
    public void testLoadList() {
        List<String> testList = new ArrayList<>();
        testList.add("Emperor");
        testList.add("King");
        testList.add("Adelie");
        testList.add("Chinstrap");
        testList.add("Macaroni");
        testList.add("Gentoo");
        MockSerializables.MockSerializable2 ms2 = new MockSerializables.MockSerializable2(42, "penguins", testList);

        ms2.updateId("test2");

        StorageToken token = ms2.saveToToken();

        MockSerializables.MockSerializable2 copy = (MockSerializables.MockSerializable2) SuperGlu_Serializable.createFromToken(token);

        Assert.assertEquals(ms2, copy);
    }


    @Test
    public void testSaveMap() {
        Map<String, Integer> testMap = new HashMap<>();

        testMap.put("Emperor", 23);
        testMap.put("King", 42);
        testMap.put("Adelie", null);

        MockSerializables.MockSerializable3 ms3 = new MockSerializables.MockSerializable3(12, "Penguins", testMap);
        ms3.updateId("test3");
        StorageToken token = ms3.saveToToken();

        System.out.println(token.toString());

        Assert.assertEquals("{\"MockSerializable3\":{\"classId\":\"MockSerializable3\",\"bar\":\"Penguins\",\"foo\":12,\"baz\":{\"map\":{\"Emperor\":23,\"King\":42,\"Adelie\":null}},\"id\":\"test3\"}}", token.toString());
    }


    @Test
    public void testLoadMap() {
        Map<String, Integer> testMap = new HashMap<>();

        testMap.put("Emperor", 23);
        testMap.put("King", 42);
        testMap.put("Adelie", null);

        MockSerializables.MockSerializable3 ms3 = new MockSerializables.MockSerializable3(12, "Penguins", testMap);
        ms3.updateId("test3");
        MockSerializables.MockSerializable3 copy = (MockSerializables.MockSerializable3) ms3.clone(false);

        Assert.assertEquals(ms3, copy);


    }


    @Test
    public void testSaveNestedClass() {
        MockSerializables.MockSerializable ms = new MockSerializables.MockSerializable(-1, "penguins");
        ms.updateId("nested");
        MockSerializables.MockSerializable4 ms4 = new MockSerializables.MockSerializable4(32, "Penguins", ms);
        ms4.updateId("test4");

        StorageToken token = ms4.saveToToken();

        System.out.println(token.toString());

        Assert.assertEquals("{\"MockSerializable4\":{\"classId\":\"MockSerializable4\",\"bar\":\"Penguins\",\"foo\":32,\"baz\":{\"MockSerializable\":{\"classId\":\"MockSerializable\",\"bar\":\"penguins\",\"foo\":-1,\"id\":\"nested\"}},\"id\":\"test4\"}}", token.toString());
    }


    @Test
    public void testLoadNestedClass() {
        MockSerializables.MockSerializable ms = new MockSerializables.MockSerializable(-1, "penguins");
        ms.updateId("nested");
        MockSerializables.MockSerializable4 ms4 = new MockSerializables.MockSerializable4(32, "Penguins", ms);
        ms4.updateId("test4");

        MockSerializables.MockSerializable4 copy = (MockSerializables.MockSerializable4) ms4.clone(false);

        Assert.assertEquals(ms4, copy);
    }


    @Test
    public void testNestedAtomic() {
        NestedAtomic nestedAtomic = new NestedAtomic(String.class, Message.ACTOR_KEY);
        StorageToken token = nestedAtomic.saveToToken();
        System.out.println(token.toString());

        NestedAtomic copy = (NestedAtomic) nestedAtomic.clone(false);

        System.out.println(copy.toString());

        Assert.assertEquals(nestedAtomic, copy);
    }
    
    
    

}
