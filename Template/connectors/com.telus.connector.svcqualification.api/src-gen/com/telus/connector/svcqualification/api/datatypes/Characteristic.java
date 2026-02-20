package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.BaseStruct;
import com.iisy.solvatio.domain.Property;

public interface Characteristic extends BaseStruct
{
	public static com.telus.connector.svcqualification.api.datatypes.Characteristic create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.CharacteristicImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.CharacteristicImpl_EXPR) TypesFactory.eINSTANCE.createCharacteristic();
		return object;
	}
	@Property("name")
	String getName();
	@Property("name")
	void setName(String value);
	@Property("value")
	String getValue();
	@Property("value")
	void setValue(String value);
} // Characteristic
