package com.telus.connector.svcqualification.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class ServicePojo {
    @JsonProperty("characteristic")
    private List<CharacteristicPojo> characteristic;
    
    @JsonProperty("place")
    private List<PlacePojo> place;
    
    @JsonProperty("eligibilityUnavailabilityReason")
    private List<EligibilityUnavailabilityReasonPojo> eligibilityUnavailabilityReason;

    // Getters and Setters
    public List<CharacteristicPojo> getCharacteristic() { return characteristic; }
    public void setCharacteristic(List<CharacteristicPojo> characteristic) { 
        this.characteristic = characteristic; 
    }
    
    public List<PlacePojo> getPlace() { return place; }
    public void setPlace(List<PlacePojo> place) { this.place = place; }
    
    public List<EligibilityUnavailabilityReasonPojo> getEligibilityUnavailabilityReason() { 
        return eligibilityUnavailabilityReason; 
    }
    public void setEligibilityUnavailabilityReason(List<EligibilityUnavailabilityReasonPojo> eligibilityUnavailabilityReason) { 
        this.eligibilityUnavailabilityReason = eligibilityUnavailabilityReason; 
    }
}