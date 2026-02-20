package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.BaseStruct;
import com.iisy.solvatio.domain.Property;

public interface EligibilityUnavailabilityReason extends BaseStruct
{
	public static com.telus.connector.svcqualification.api.datatypes.EligibilityUnavailabilityReason create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.EligibilityUnavailabilityReasonImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.EligibilityUnavailabilityReasonImpl_EXPR) TypesFactory.eINSTANCE.createEligibilityUnavailabilityReason();
		return object;
	}
	@Property("label")
	String getLabel();
	@Property("label")
	void setLabel(String value);
	@Property("code")
	Integer getCode();
	@Property("code")
	void setCode(Integer value);
} // EligibilityUnavailabilityReason
