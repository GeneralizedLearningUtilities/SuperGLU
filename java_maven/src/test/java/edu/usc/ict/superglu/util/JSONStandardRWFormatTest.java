package edu.usc.ict.superglu.util;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

import org.junit.After;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;

import edu.usc.ict.superglu.util.tokenformat.JSONStandardRWFormat;

public class JSONStandardRWFormatTest {

	@Before
	public void setUp() throws Exception {
	}

	@After
	public void tearDown() throws Exception {
	}

	@Test
	public void testParse() {
		String input = ("{\"classID\":{\"float1\":3.14,\"nullVal\":null,\"classId\":\"classID\",\"int1\":10,\"str1\":\"value\",\"id\":\"id\",\"bool1\":true}}");
		
		StorageToken token = JSONStandardRWFormat.parse(input);
		
		String result = JSONStandardRWFormat.serialize(token);
		
		Assert.assertEquals(input, result);
	}
	
	
	@Test
	public void testParseList() {
		String input = "{\"classID\":{\"classId\":\"classID\",\"stringList\":[\"string1\",\"string2\",\"string3\"],\"id\":\"id\"}}";
		
		StorageToken token = JSONStandardRWFormat.parse(input);
		
		String result = JSONStandardRWFormat.serialize(token);
		
		Assert.assertEquals(input, result);
	}

	
	@Test
	public void testParseMap() {
		String input = "{\"classID\":{\"classId\":\"classID\",\"stringIntMap\":{\"key1\":13,\"key2\":32,\"key3\":1300,\"isMap\":true},\"id\":\"id\"}}";
		
		StorageToken token = JSONStandardRWFormat.parse(input);
		
		String result = JSONStandardRWFormat.serialize(token);
		
		Assert.assertEquals(input, result);
	}
	
	
	@Test
	public void testParseNestedObject()
	{
		String input = "{\"TestData\":{\"classId\":\"TestData\",\"innerTokens\":[{\"classID1\":{\"float1\":3.14,\"classId\":\"classID1\",\"int1\":10,\"str1\":\"value\",\"id\":\"id1\",\"bool1\":true}},{\"classID2\":{\"float1\":43212,\"classId\":\"classID2\",\"int1\":1113,\"str1\":\"value2\",\"id\":\"id2\",\"bool1\":true}}],\"id\":\"outerToken\"}}";
		
		StorageToken token = JSONStandardRWFormat.parse(input);
		
		String result = JSONStandardRWFormat.serialize(token);
		
		Assert.assertEquals(input, result);
	}
	
	
	@Test
	public void testSerializeStorageToken() {
		Map<String, Object> data = new HashMap<>();
		data.put("str1", "value");
		data.put("int1", 10);
		data.put("float1", 3.14);
		data.put("bool1", true);
		data.put("nullVal", null);
		StorageToken token = new StorageToken(data, "id", "classID");
		
		String json = JSONStandardRWFormat.serialize(token);
		
		Assert.assertEquals("{\"classID\":{\"float1\":3.14,\"nullVal\":null,\"classId\":\"classID\",\"int1\":10,\"str1\":\"value\",\"id\":\"id\",\"bool1\":true}}", json);
		
		System.out.println(json);
	}
	
	
	@Test
	public void testSerializeList()
	{
		Map<String, Object> data = new HashMap<>();
		List<String> stringList = new ArrayList<>();
		
		stringList.add("string1");
		stringList.add("string2");
		stringList.add("string3");
		data.put("stringList", stringList);
		
		
		
		StorageToken token = new StorageToken(data, "id", "classID");
		
		String json = JSONStandardRWFormat.serialize(token);
		
		Assert.assertEquals("{\"classID\":{\"classId\":\"classID\",\"stringList\":[\"string1\",\"string2\",\"string3\"],\"id\":\"id\"}}", json);
		
		System.out.println(json);
	}
	
	
	@Test
	public void testSerializeMap()
	{
		Map<String, Object> data = new HashMap<>();
		Map<String, Integer> map = new HashMap<String, Integer>();
		
		map.put("key1", 13);
		map.put("key2", 32);
		map.put("key3", 1300);
		data.put("stringIntMap", map);
		
		
		
		StorageToken token = new StorageToken(data, "id", "classID");
		
		String json = JSONStandardRWFormat.serialize(token);
		
		Assert.assertEquals("{\"classID\":{\"classId\":\"classID\",\"stringIntMap\":{\"key1\":13,\"key2\":32,\"key3\":1300,\"isMap\":true},\"id\":\"id\"}}", json);
		
		System.out.println(json);
	}
	
	
	@Test
	public void testSerializeNestedObjects()
	{
		Map<String, Object> data = new HashMap<>();
		data.put("str1", "value");
		data.put("int1", 10);
		data.put("float1", 3.14);
		data.put("bool1", true);
		StorageToken innerToken1 = new StorageToken(data, "id1", "classID1");
		
		Map<String, Object> data2 = new HashMap<>();
		data2.put("str1", "value2");
		data2.put("int1", 1113);
		data2.put("float1", 43212);
		data2.put("bool1", true);
		StorageToken innerToken2 = new StorageToken(data2, "id2", "classID2");
		
		List<StorageToken> innerTokens = new ArrayList<>();
		innerTokens.add(innerToken1);
		innerTokens.add(innerToken2);
		
		Map<String, Object> outerData = new HashMap<>();
		outerData.put("innerTokens", innerTokens);
		StorageToken outerToken = new StorageToken(outerData, "outerToken", "TestData");
		
		String json = JSONStandardRWFormat.serialize(outerToken);

		Assert.assertEquals("{\"TestData\":{\"classId\":\"TestData\",\"innerTokens\":[{\"classID1\":{\"float1\":3.14,\"classId\":\"classID1\",\"int1\":10,\"str1\":\"value\",\"id\":\"id1\",\"bool1\":true}},{\"classID2\":{\"float1\":43212,\"classId\":\"classID2\",\"int1\":1113,\"str1\":\"value2\",\"id\":\"id2\",\"bool1\":true}}],\"id\":\"outerToken\"}}", json);
		
		System.out.println(json);
		
		
		
		
	}

}
