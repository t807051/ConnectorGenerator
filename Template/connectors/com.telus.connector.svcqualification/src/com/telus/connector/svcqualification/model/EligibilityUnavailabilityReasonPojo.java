package com.telus.connector.svcqualification.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class EligibilityUnavailabilityReasonPojo {
    @JsonProperty("label")
    private String label;
    
    @JsonProperty("code")
    private Integer code;

    // Getters and Setters
    public String getLabel() { return label; }
    public void setLabel(String label) { this.label = label; }
    
    public Integer getCode() { return code; }
    public void setCode(Integer code) { this.code = code; }
}