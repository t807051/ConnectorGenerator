package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.BaseStruct;
import com.iisy.solvatio.domain.Property;
import java.util.Collection;
import java.util.List;

public interface GetSvcQualificationEntity extends BaseStruct
{
	public static com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationEntity create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.GetSvcQualificationEntityImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.GetSvcQualificationEntityImpl_EXPR) TypesFactory.eINSTANCE.createGetSvcQualificationEntity();
		return object;
	}
	@Property("id")
	String getId();
	@Property("id")
	void setId(String value);
	@Property("qualificationResult")
	String getQualificationResult();
	@Property("qualificationResult")
	void setQualificationResult(String value);
	@Property("externalId")
	String getExternalId();
	@Property("externalId")
	void setExternalId(String value);
	@Property("description")
	String getDescription();
	@Property("description")
	void setDescription(String value);
	@Property("serviceQualificationItem")
	List<ServiceQualificationItem> getServiceQualificationItem();
	@Property("serviceQualificationItem")
	void setServiceQualificationItem(Collection<? extends ServiceQualificationItem> value);
} // GetSvcQualificationEntity
