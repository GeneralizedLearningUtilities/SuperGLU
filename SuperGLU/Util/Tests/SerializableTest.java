package Util.Tests;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.junit.Assert;
import org.junit.Test;

import Core.Message;
import Ontology.Mappings.NestedAtomic;
import Util.Serializable;
import Util.StorageToken;
import Util.Tests.MockSerializables.MockSerializable;
import Util.Tests.MockSerializables.MockSerializable2;
import Util.Tests.MockSerializables.MockSerializable3;
import Util.Tests.MockSerializables.MockSerializable4;

public class SerializableTest {
	
	@Test
	public void testReflection() {
		Serializable.populateClassIDs(null);
	}
	
	
	@Test
	public void testSaveToStorageToken()
	{
		MockSerializable ms = new MockSerializables.MockSerializable(-1, "penguins");
		ms.updateId("test1");
		StorageToken token = ms.saveToToken();
		System.out.println(token.toString());
		
		Assert.assertEquals("{\"MockSerializable\":{\"classId\":\"MockSerializable\",\"bar\":\"penguins\",\"foo\":-1,\"id\":\"test1\"}}", token.toString());
	}
	
	
	@Test
	public void testLoadFromStorageToken()
	{
		MockSerializable ms = new MockSerializable(-1, "penguins");
		StorageToken token = ms.saveToToken();
		MockSerializable copy = (MockSerializable) Serializable.createFromToken(token);
		
		Assert.assertEquals(ms, copy);
	}
	
	
	@Test
	public void testSaveList()
	{
		List<String> testList = new ArrayList<>();
		testList.add("Emperor");
		testList.add("King");
		testList.add("Adelie");
		testList.add("Chinstrap");
		testList.add("Macaroni");
		testList.add("Gentoo");
		MockSerializable2 ms2 = new MockSerializable2(42, "penguins", testList);
		
		ms2.updateId("test2");
		
		StorageToken token = ms2.saveToToken();
		
		System.out.println(token.toString());
		Assert.assertEquals("{\"MockSerializable2\":{\"classId\":\"MockSerializable2\",\"bar\":\"penguins\",\"foo\":42,\"baz\":{\"list\":[\"Emperor\",\"King\",\"Adelie\",\"Chinstrap\",\"Macaroni\",\"Gentoo\"]},\"id\":\"test2\"}}", token.toString());
	}
	
	
	@Test
	public void testLoadList()
	{
		List<String> testList = new ArrayList<>();
		testList.add("Emperor");
		testList.add("King");
		testList.add("Adelie");
		testList.add("Chinstrap");
		testList.add("Macaroni");
		testList.add("Gentoo");
		MockSerializable2 ms2 = new MockSerializable2(42, "penguins", testList);
		
		ms2.updateId("test2");
		
		StorageToken token = ms2.saveToToken();
		
		MockSerializable2 copy = (MockSerializable2) Serializable.createFromToken(token);
		
		Assert.assertEquals(ms2, copy);	
	}
	
	
	@Test
	public void testSaveMap()
	{
		Map<String, Integer> testMap = new HashMap<>();
		
		testMap.put("Emperor", 23);
		testMap.put("King", 42);
		testMap.put("Adelie", null);
		
		MockSerializable3 ms3 = new MockSerializable3(12, "Penguins", testMap);
		ms3.updateId("test3");
		StorageToken token = ms3.saveToToken();
		
		System.out.println(token.toString());
		
		Assert.assertEquals("{\"MockSerializable3\":{\"classId\":\"MockSerializable3\",\"bar\":\"Penguins\",\"foo\":12,\"baz\":{\"map\":{\"Emperor\":23,\"King\":42,\"Adelie\":null}},\"id\":\"test3\"}}", token.toString());
	}
	
	
	@Test
	public void testLoadMap()
	{
		Map<String, Integer> testMap = new HashMap<>();
		
		testMap.put("Emperor", 23);
		testMap.put("King", 42);
		testMap.put("Adelie", null);
		
		MockSerializable3 ms3 = new MockSerializable3(12, "Penguins", testMap);
		ms3.updateId("test3");
		MockSerializable3 copy = (MockSerializable3) ms3.clone(false);
		
		Assert.assertEquals(ms3, copy);
		
		
	}
	
	
	@Test
	public void testSaveNestedClass()
	{
		MockSerializable ms = new MockSerializable(-1, "penguins");
		ms.updateId("nested");
		MockSerializable4 ms4 = new MockSerializable4(32, "Penguins", ms);
		ms4.updateId("test4");
		
		StorageToken token = ms4.saveToToken();
		
		System.out.println(token.toString());
		
		Assert.assertEquals("{\"MockSerializable4\":{\"classId\":\"MockSerializable4\",\"bar\":\"Penguins\",\"foo\":32,\"baz\":{\"MockSerializable\":{\"classId\":\"MockSerializable\",\"bar\":\"penguins\",\"foo\":-1,\"id\":\"nested\"}},\"id\":\"test4\"}}",  token.toString());		
	}
	
	
	@Test
	public void testLoadNestedClass()
	{
		MockSerializable ms = new MockSerializable(-1, "penguins");
		ms.updateId("nested");
		MockSerializable4 ms4 = new MockSerializable4(32, "Penguins", ms);
		ms4.updateId("test4");
		
		MockSerializable4 copy = (MockSerializable4) ms4.clone(false);
		
		Assert.assertEquals(ms4, copy);
	}
	
	
	@Test
	public void testNestedAtomic()
	{
	    NestedAtomic nestedAtomic = new NestedAtomic(String.class, Message.ACTOR_KEY);
	    StorageToken token = nestedAtomic.saveToToken();
	    System.out.println(token.toString());
	    
	    NestedAtomic copy = (NestedAtomic) nestedAtomic.clone(false);
	    
	    Assert.assertEquals(nestedAtomic, copy);
	}

}
