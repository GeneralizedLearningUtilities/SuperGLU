package Ontology.Converters;

import Util.Serializable;

/**
 * This class is a dummy converter for times when we don't actually need to convert anything
 * @author auerbach
 *
 */
public class DummyConverter extends Serializable implements DataConverter {

	@Override
	public boolean isApplicable(Object input) {
		return true;
	}

	@Override
	public Object convert(Object input, Object context) {
		return input;
	}

}
