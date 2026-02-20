package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.BaseStruct;
import com.iisy.solvatio.domain.Property;

public interface GetSvcQualificationRequest extends BaseStruct
{
	public static com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.GetSvcQualificationRequestImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.GetSvcQualificationRequestImpl_EXPR) TypesFactory.eINSTANCE.createGetSvcQualificationRequest();
		return object;
	}
	@Property("lpdsId")
	String getLpdsId();
	@Property("lpdsId")
	void setLpdsId(String value);
} // GetSvcQualificationRequest
