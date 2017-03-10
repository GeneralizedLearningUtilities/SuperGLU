package Ontology.Mappings.Tests;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import Ontology.Converters.DataConverter;
import Ontology.Converters.SpaceSeparation;
import Ontology.Mappings.NestedSubAtomic;
import Util.Pair;
import Util.SerializationConvenience;
import Util.SerializationFormatEnum;
import Util.StorageToken;

public class NestedSubAtomicTest
{
    private NestedSubAtomic nestedSubAtomic;
    
    private StorageToken sampleData;

    @Before
    public void setUp() throws Exception
    {
	List<Pair<Class<?>, String>> indices = new ArrayList<>();
	indices.add(new Pair<Class<?>, String>(String.class, "foo"));
	DataConverter converter = new SpaceSeparation();
	nestedSubAtomic = new NestedSubAtomic(indices, converter, 1);
	
	String foo = "test pass";
	sampleData = new StorageToken();
	sampleData.setItem("foo", foo);
	
    }

    @After
    public void tearDown() throws Exception
    {
	this.nestedSubAtomic = null;
	this.sampleData = null;
    }

    @Test
    public void testSaveToToken()
    {
	String serialized = SerializationConvenience.serializeObject(nestedSubAtomic, SerializationFormatEnum.JSON_FORMAT);
	NestedSubAtomic copy = (NestedSubAtomic) SerializationConvenience.nativeizeObject(serialized, SerializationFormatEnum.JSON_FORMAT);
	
	Assert.assertEquals(nestedSubAtomic, copy);
    }

    @Test
    public void testRetrieveFieldData()
    {
	String data = (String)nestedSubAtomic.retrieveFieldData(sampleData);
	Assert.assertEquals("pass", data);
    }

    @Test
    public void testStoreData()
    {
	StorageToken token = new StorageToken(new HashMap<>(), "testToken", "none");
	
	nestedSubAtomic.storeData(token, "pass");
	
	String result = (String)nestedSubAtomic.retrieveFieldData(token);
	
	Assert.assertEquals("pass", result);
	
    }
    
    
    @Test
    public void testOutOfOrderStorage()
    {
	List<Pair<Class<?>, String>> indices = new ArrayList<>();
	indices.add(new Pair<Class<?>, String>(String.class, "foo"));
	DataConverter converter = new SpaceSeparation();
	NestedSubAtomic otherNestedSubAtomic = new NestedSubAtomic(indices, converter, 0);
	
	StorageToken token = new StorageToken(new HashMap<>(), "testToken", "none");
	
	nestedSubAtomic.storeData(token, "pass");
	otherNestedSubAtomic.storeData(token, "test");
	
	String firstResult = (String)nestedSubAtomic.retrieveFieldData(token);
	String secondResult = (String)otherNestedSubAtomic.retrieveFieldData(token);
	
	Assert.assertEquals("pass", firstResult);
	Assert.assertEquals("test", secondResult);
    }

}
