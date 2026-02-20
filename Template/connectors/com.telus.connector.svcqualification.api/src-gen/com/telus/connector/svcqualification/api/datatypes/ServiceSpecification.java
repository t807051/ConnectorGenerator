package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.BaseStruct;
import com.iisy.solvatio.domain.Property;

public interface ServiceSpecification extends BaseStruct
{
	public static com.telus.connector.svcqualification.api.datatypes.ServiceSpecification create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.ServiceSpecificationImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.ServiceSpecificationImpl_EXPR) TypesFactory.eINSTANCE.createServiceSpecification();
		return object;
	}
	@Property("name")
	String getName();
	@Property("name")
	void setName(String value);
} // ServiceSpecification
