package com.telus.connector.svcqualification.api.datatypes;

import com.iisy.solvatio.domain.BaseStruct;
import com.iisy.solvatio.domain.Property;
import java.util.Collection;
import java.util.List;

public interface Service extends BaseStruct
{
	public static com.telus.connector.svcqualification.api.datatypes.Service create()
	{
		com.telus.connector.svcqualification.api.datatypes.impl.ServiceImpl_EXPR object = (com.telus.connector.svcqualification.api.datatypes.impl.ServiceImpl_EXPR) TypesFactory.eINSTANCE.createService();
		return object;
	}
	@Property("characteristic")
	List<Characteristic> getCharacteristic();
	@Property("place")
	List<Place> getPlace();
	@Property("eligibilityUnavailabilityReason")
	List<EligibilityUnavailabilityReason> getEligibilityUnavailabilityReason();
	@Property("characteristic")
	void setCharacteristic(Collection<? extends Characteristic> value);
	@Property("place")
	void setPlace(Collection<? extends Place> value);
	@Property("eligibilityUnavailabilityReason")
	void setEligibilityUnavailabilityReason(Collection<? extends EligibilityUnavailabilityReason> value);
} // Service
