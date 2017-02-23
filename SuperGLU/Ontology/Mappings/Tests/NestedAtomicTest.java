package Ontology.Mappings.Tests;

import static org.junit.Assert.*;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import Ontology.Mappings.NestedAtomic;
import Util.Pair;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;
import Util.StorageToken;

public class NestedAtomicTest
{
    
    private NestedAtomic nestedAtomic;

    private StorageToken sampleData;
    
    
    @Before
    public void setUp() throws Exception
    {
	List<Pair<Class<?>, String>> indices = new ArrayList<>();
	indices.add(new Pair<Class<?>, String>(StorageToken.class, "innerStorageToken"));
	indices.add(new Pair<Class<?>, String>(HashMap.class, "testHashMap"));
	indices.add(new Pair<Class<?>, String>(ArrayList.class, "testList"));
	indices.add(new Pair<Class<?>, String>(String.class, "0"));
	nestedAtomic = new NestedAtomic(indices);
	
	
	String zero = "pass";
	List<Object> testList = new ArrayList<>();
	testList.add(zero);
	Map<String, Object> testHashMap = new HashMap<>();
	testHashMap.put("testList", testList);
	sampleData = new StorageToken();
	StorageToken innerStorageToken = new StorageToken();
	innerStorageToken.setItem("testHashMap", testHashMap);
	sampleData.setItem("innerStorageToken", innerStorageToken);
	
    }

    @After
    public void tearDown() throws Exception
    {
	this.sampleData = null;
	this.nestedAtomic = null;
    }

    @Test
    public void testInitializeFromToken()
    {
	NestedAtomic copy = (NestedAtomic) this.nestedAtomic.clone(false);
	Assert.assertTrue(nestedAtomic.equals(copy));
    }


    @Test
    public void testRetrieveFieldData()
    {
	String result = (String)nestedAtomic.retrieveFieldData(sampleData);
	Assert.assertEquals("pass", result);
    }

    @Test
    public void testStoreData()
    {
	nestedAtomic.storeData(sampleData, "pass2");
	String result = (String)nestedAtomic.retrieveFieldData(sampleData);
	Assert.assertEquals("pass2", result);

    }

}
