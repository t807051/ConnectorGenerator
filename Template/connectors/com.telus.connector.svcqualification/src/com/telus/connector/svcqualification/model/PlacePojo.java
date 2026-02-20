package com.telus.connector.svcqualification.model;

import com.fasterxml.jackson.annotation.JsonProperty;

public class PlacePojo {
    @JsonProperty("role")
    private String role;
    
    @JsonProperty("id")
    private Object id; // Can be Long or String

    // Getters and Setters
    public String getRole() { return role; }
    public void setRole(String role) { this.role = role; }
    
    public Object getId() { return id; }
    public void setId(Object id) { this.id = id; }
}