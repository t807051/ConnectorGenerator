package com.telus.connector.svcqualification.converter;

import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Collection;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import java.util.Locale;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.module.SimpleModule;
import com.solvatio.connector.rest.common.domaininterface.conversion.ConversionException;
import com.solvatio.connector.rest.common.domaininterface.conversion.Converter;
import com.telus.common.api.datatypes.MacAddress;
import com.telus.common.api.helper.MacAddressHelper;
import com.telus.connector.svcqualification.api.datatypes.Characteristic;
import com.telus.connector.svcqualification.api.datatypes.EligibilityUnavailabilityReason;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationEntity;
import com.telus.connector.svcqualification.api.datatypes.Place;
import com.telus.connector.svcqualification.api.datatypes.Service;
import com.telus.connector.svcqualification.api.datatypes.ServiceQualificationItem;
import com.telus.connector.svcqualification.api.datatypes.ServiceSpecification;
import com.telus.connector.svcqualification.exception.GetSvcQualificationConversionException;
import com.telus.connector.svcqualification.model.*;

public class GetSvcQualificationConverter implements Converter<JsonNode, GetSvcQualificationEntity>{
	private final ObjectMapper mapper;
	
	public GetSvcQualificationConverter() {
		this.mapper = new ObjectMapper();
    }
	
	@Override
	public GetSvcQualificationEntity convert(JsonNode input) throws ConversionException {
		GetSvcQualificationEntity rv = null;
		if (input == null) 
			return rv;

		try {
			ServiceQualificationPojo sq = mapper.treeToValue(input, ServiceQualificationPojo.class);
			rv = toGetSvcQualificationEntity(sq);
		} catch (Exception e) {
			GetSvcQualificationConversionException ex = new GetSvcQualificationConversionException(e.getMessage()); 
			throw ex;
		}
		
		return rv;
	}


	private GetSvcQualificationEntity toGetSvcQualificationEntity(ServiceQualificationPojo sq) {
		if (sq == null) return null;
		GetSvcQualificationEntity rv = GetSvcQualificationEntity.create();
		rv.setExternalId(sq.getExternalId());
		rv.setDescription(sq.getDescription());
		rv.setId(toString(sq.getId()));
		rv.setQualificationResult(sq.getQualificationResult());
		rv.setServiceQualificationItem(toServiceQualificationItem(sq.getServiceQualificationItem()));
		return rv;
	}

	private List<ServiceQualificationItem> toServiceQualificationItem(
			List<ServiceQualificationItemPojo> serviceQualificationItem) {
		List<ServiceQualificationItem> rv = new ArrayList<ServiceQualificationItem>();
		if (serviceQualificationItem == null)
			return rv;
		for (com.telus.connector.svcqualification.model.ServiceQualificationItemPojo i : safe(serviceQualificationItem)) {
			ServiceQualificationItem sqi = toServiceQualificationItem(i);
			if (sqi != null)
				rv.add(sqi);
		}
		return rv;
	}

	private ServiceQualificationItem toServiceQualificationItem(ServiceQualificationItemPojo item) {
		if (item == null)
			return null;
		ServiceQualificationItem rv = ServiceQualificationItem.create();
		rv.setExpectedServiceAvailabilityDate(item.getExpectedServiceAvailabilityDate());
		rv.setId(""+item.getId());
		rv.setQualificationResult(item.getQualificationResult());
		rv.setService(toService(item.getService()));
		rv.setServiceSpecification(toServiceSpecification(item.getServiceSpecification()));
		return rv;
	}

	private ServiceSpecification toServiceSpecification(ServiceSpecificationPojo serviceSpecification) {
		if (serviceSpecification == null)
			return null;
		ServiceSpecification rv = ServiceSpecification.create();
		rv.setName(serviceSpecification.getName());
		return rv;
	}

	private Service toService(ServicePojo service) {
		if (service == null)
			return null;
		Service rv = Service.create();
		rv.setCharacteristic(toCharacteristicList(service.getCharacteristic()));
		rv.setEligibilityUnavailabilityReason(toEligibilityUnavailabilityReasonList(service.getEligibilityUnavailabilityReason()));
		rv.setPlace(toPlaceList(service.getPlace()));
		return rv;
	}

	private List<Place> toPlaceList(List<PlacePojo> place) {
		List<Place> rv = new ArrayList<Place>();
		if (place == null)
			return null;
		for (PlacePojo i : safe(place)) {
			Place r = Place.create();
			r.setId(""+i.getId());
			r.setRole(i.getRole());
			rv.add(r);
		}
		return rv;
	}

	private List<Characteristic> toCharacteristicList(List<CharacteristicPojo> input) {
		List<Characteristic> rv = new ArrayList<Characteristic>();
		if (input == null)
			return rv;
		for (CharacteristicPojo i : safe(input)) {
			Characteristic r = toCharacteristic(i);
			if (r != null)
				rv.add(r);
		}
		return rv;
	}

	private Characteristic toCharacteristic(CharacteristicPojo item) {
		if (item == null)
			return null;
		Characteristic rv = Characteristic.create();
		rv.setName(item.getName());
		rv.setValue(""+item.getValue());
		return rv;
	}

	private List<EligibilityUnavailabilityReason> toEligibilityUnavailabilityReasonList(
			List<EligibilityUnavailabilityReasonPojo> input) {
		List<EligibilityUnavailabilityReason> rv = new ArrayList<EligibilityUnavailabilityReason>();
		if (input == null)
			return rv;
		
		for (EligibilityUnavailabilityReasonPojo i : safe(input)) {
			EligibilityUnavailabilityReason r = toEligibilityUnavailabilityReason(i);
			if (r != null)
				rv.add(r);
		}
		return rv;
	}

	private EligibilityUnavailabilityReason toEligibilityUnavailabilityReason(EligibilityUnavailabilityReasonPojo item) {
		if (item == null)
			return null;
		EligibilityUnavailabilityReason rv = EligibilityUnavailabilityReason.create();
		rv.setCode(item.getCode());
		rv.setLabel(item.getLabel());
		return rv;
	}

	private String toString(Long id) {
		try {
			return id.toString();
		} catch (Exception e) {
			return null;
		}
	}

	/**
	 * Make for loops safe by returning an empty list if the list is null
	 */
	private static <T> Iterable<T> safe(Iterable<T> iterable) {
		return iterable == null ? Collections.<T>emptyList() : iterable;
	}

    public static Date parseDateFormat(String date){
    	String DATE_FORMAT = "MMM dd, yyyy, h:mm:ss a";

    	if (date != null && date != ""){
    		try {
    			Locale locale = Locale.CANADA;
				SimpleDateFormat format = new SimpleDateFormat(DATE_FORMAT, locale);
    			Date parsedDate = format.parse(date);
    			
    			return parsedDate;
    		}   catch(Exception e) {
    			return null; //any failure
    		}
    	}
    	return null;
    }


}
