package com.telus.connector.svcqualification.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class ServiceSpecificationPojo {
    @JsonProperty("name")
    private String name;

    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
}