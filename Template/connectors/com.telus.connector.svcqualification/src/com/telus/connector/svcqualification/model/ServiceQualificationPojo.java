package com.telus.connector.svcqualification.model;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;

public class ServiceQualificationPojo {
    @JsonProperty("id")
    private Long id;
    
    @JsonProperty("qualificationResult")
    private String qualificationResult;
    
    @JsonProperty("externalId")
    private String externalId;
    
    @JsonProperty("description")
    private String description;
    
    @JsonProperty("serviceQualificationItem")
    private List<ServiceQualificationItemPojo> serviceQualificationItem;

    // Getters and Setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    
    public String getQualificationResult() { return qualificationResult; }
    public void setQualificationResult(String qualificationResult) { this.qualificationResult = qualificationResult; }
    
    public String getExternalId() { return externalId; }
    public void setExternalId(String externalId) { this.externalId = externalId; }
    
    public String getDescription() { return description; }
    public void setDescription(String description) { this.description = description; }
    
    public List<ServiceQualificationItemPojo> getServiceQualificationItem() { return serviceQualificationItem; }
    public void setServiceQualificationItem(List<ServiceQualificationItemPojo> serviceQualificationItem) { 
        this.serviceQualificationItem = serviceQualificationItem; 
    }
}