package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.BaseStruct;
import com.iisy.solvatio.domain.Property;

public interface ServiceQualificationItem extends BaseStruct
{
	public static com.telus.connector.svcqualification.api.datatypes.ServiceQualificationItem create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.ServiceQualificationItemImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.ServiceQualificationItemImpl_EXPR) TypesFactory.eINSTANCE.createServiceQualificationItem();
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
	@Property("expectedServiceAvailabilityDate")
	String getExpectedServiceAvailabilityDate();
	@Property("expectedServiceAvailabilityDate")
	void setExpectedServiceAvailabilityDate(String value);
	@Property("serviceSpecification")
	ServiceSpecification getServiceSpecification();
	@Property("serviceSpecification")
	void setServiceSpecification(ServiceSpecification value);
	@Property("service")
	Service getService();
	@Property("service")
	void setService(Service value);
} // ServiceQualificationItem
