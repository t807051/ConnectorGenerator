package com.telus.connector.svcqualification.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ServiceQualificationItemPojo {
    @JsonProperty("id")
    private Object id; // Can be Long or String
    
    @JsonProperty("qualificationResult")
    private String qualificationResult;
    
    @JsonProperty("expectedServiceAvailabilityDate")
    private String expectedServiceAvailabilityDate;
    
    @JsonProperty("serviceSpecification")
    private ServiceSpecificationPojo serviceSpecification;
    
    @JsonProperty("service")
    private ServicePojo service;

    // Getters and Setters
    public Object getId() { return id; }
    public void setId(Object id) { this.id = id; }
    
    public String getQualificationResult() { return qualificationResult; }
    public void setQualificationResult(String qualificationResult) { this.qualificationResult = qualificationResult; }
    
    public String getExpectedServiceAvailabilityDate() { return expectedServiceAvailabilityDate; }
    public void setExpectedServiceAvailabilityDate(String expectedServiceAvailabilityDate) { 
        this.expectedServiceAvailabilityDate = expectedServiceAvailabilityDate; 
    }
    
    public ServiceSpecificationPojo getServiceSpecification() { return serviceSpecification; }
    public void setServiceSpecification(ServiceSpecificationPojo serviceSpecification) { 
        this.serviceSpecification = serviceSpecification; 
    }
    
    public ServicePojo getService() { return service; }
    public void setService(ServicePojo service) { this.service = service; }
}