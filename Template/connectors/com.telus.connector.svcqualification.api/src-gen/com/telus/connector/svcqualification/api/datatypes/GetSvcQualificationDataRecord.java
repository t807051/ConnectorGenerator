package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.Property;
import com.telus.common.api.datatypes.AbstractDataRecord;

public interface GetSvcQualificationDataRecord extends AbstractDataRecord
{
	public static com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationDataRecord create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.GetSvcQualificationDataRecordImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.GetSvcQualificationDataRecordImpl_EXPR) TypesFactory.eINSTANCE.createGetSvcQualificationDataRecord();
		return object;
	}
	@Property("svcQualificationEntity")
	GetSvcQualificationEntity getSvcQualificationEntity();
	@Property("svcQualificationEntity")
	void setSvcQualificationEntity(GetSvcQualificationEntity value);
} // GetSvcQualificationDataRecord
