package com.telus.connector.svcqualification;

import com.solvatio.connector.rest.common.config.IRestConnectorConfigurationComponent;

public interface ISvcQualificationConfigurationComponent extends IRestConnectorConfigurationComponent {
	public String getTargetEnv();
}
