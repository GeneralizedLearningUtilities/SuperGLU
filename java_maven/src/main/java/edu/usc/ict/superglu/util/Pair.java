package edu.usc.ict.superglu.util;

/**
 * Simple implementation of a tuple with two values
 *
 * @param <T> Type of First value
 * @param <U> Type of Second Value
 * @author auerbach
 */

public class Pair<T, U> extends SuperGlu_Serializable {

    public static String FIRST_KEY = "first";
    public static String SECOND_KEY = "second";

    private T first;
    private U second;

    public Pair(T first, U second) {
        this.first = first;
        this.second = second;
    }


    public Pair() {
        this.first = null;
        this.second = null;
    }

    public T getFirst() {
        return this.first;
    }

    public U getSecond() {
        return this.second;
    }

    public void setFirst(T first) {
        this.first = first;
    }

    public void setSecond(U second) {
        this.second = second;
    }

    // Equality Operations
    @Override
    public boolean equals(Object otherObject) {
        if (!super.equals(otherObject))
            return false;

        if (!(otherObject instanceof Pair))
            return false;

        Pair<T, U> other = (Pair<T, U>) otherObject;

        if (!fieldIsEqual(this.first, other.first))
            return false;

        if (!fieldIsEqual(this.second, other.second))
            return false;

        return true;
    }

    @Override
    public int hashCode() {
        int result = super.hashCode();
        int arbitraryPrimeNumber = 23;

        if (this.first != null)
            result = result * arbitraryPrimeNumber + this.first.hashCode();

        if (this.second != null)
            result = result * arbitraryPrimeNumber + this.second.hashCode();

        return result;

    }

    // Serialization/Deserialization
    @Override
    public void initializeFromToken(StorageToken token) {
        super.initializeFromToken(token);
        this.first = (T) SerializationConvenience.untokenizeObject(token.getItem(FIRST_KEY));
        this.second = (U) SerializationConvenience.untokenizeObject(token.getItem(SECOND_KEY));

    }

    @Override
    public StorageToken saveToToken() {
        StorageToken result = super.saveToToken();
        result.setItem(FIRST_KEY, SerializationConvenience.tokenizeObject(this.first));
        result.setItem(SECOND_KEY, SerializationConvenience.tokenizeObject(this.second));
        return result;
    }
}
