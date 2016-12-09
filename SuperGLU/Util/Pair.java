package Util;

/**
 * Simple implementation of a tuple with two values
 * @author auerbach
 *
 * @param <T> Type of First value
 * @param <U> Type of Second Value
 */

public class Pair<T, U> {

	private T first;
	private U second;
	
	public Pair(T first, U second)
	{
		this.first = first;
		this.second = second;
	}
	
	
	public T getFirst()
	{
		return this.first;
	}
	
	
	public U getSecond()
	{
		return this.second;
	}
	
}
