package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.BaseStruct;
import com.iisy.solvatio.domain.Property;

public interface Place extends BaseStruct
{
	public static com.telus.connector.svcqualification.api.datatypes.Place create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.PlaceImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.PlaceImpl_EXPR) TypesFactory.eINSTANCE.createPlace();
		return object;
	}
	@Property("role")
	String getRole();
	@Property("role")
	void setRole(String value);
	@Property("id")
	String getId();
	@Property("id")
	void setId(String value);
} // Place
