package com.telus.connector.svcqualification.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class CharacteristicPojo {
    @JsonProperty("name")
    private String name;
    
    @JsonProperty("value")
    private Object value; // Can be String, Boolean, Number, or null

    // Getters and Setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    
    public Object getValue() { return value; }
    public void setValue(Object value) { this.value = value; }
}