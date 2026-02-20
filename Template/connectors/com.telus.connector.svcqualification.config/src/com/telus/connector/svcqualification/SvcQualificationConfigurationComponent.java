package com.telus.connector.svcqualification;

import java.util.Map;

import javax.ws.rs.client.Client;
import javax.ws.rs.client.ClientBuilder;

import org.glassfish.jersey.client.ClientConfig;
import org.osgi.service.cm.ConfigurationException;
import org.osgi.service.component.annotations.Activate;
import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.ConfigurationPolicy;

import com.solvatio.connector.rest.common.config.RestConnectorConfigurationComponent;
import com.solvatio.connector.rest.common.config.jersey.JerseyConnectorConfiguration;
import com.solvatio.connector.rest.common.logging.SLF4JFeature;

@Component(service = ISvcQualificationConfigurationComponent.class, 
			immediate = true, name = "com.telus.connector.svcqualification.SvcQualification", 
			property = "target=com.telus.connector.svcqualification.SvcQualification", 
			configurationPid = "com.telus.connector.svcqualification.SvcQualification.rest", 
			configurationPolicy = ConfigurationPolicy.REQUIRE)
public class SvcQualificationConfigurationComponent extends RestConnectorConfigurationComponent implements ISvcQualificationConfigurationComponent {

	public static final String ID = "com.telus.connector.svcqualification.SvcQualification";
	public static final String CONFIGURATION_PID = SvcQualificationConfigurationComponent.ID
			+ RestConnectorConfigurationComponent.POSTFIX;
	private String targetEnv;

	public SvcQualificationConfigurationComponent() {
		super(ID);
	}

	@Activate
	protected synchronized void configure(Map<String, Object> config) throws ConfigurationException {
		this.connectorConfiguration = loadConfiguration(config);
		
		ClientConfig clientConfig = JerseyConnectorConfiguration.create(this.connectorConfiguration, this.logger);

		Client client = ClientBuilder.newClient(clientConfig);
		client.register(new SLF4JFeature(this.logger));

		this.webTarget = client.target(this.connectorConfiguration.getEndpoint());
		this.setTargetEnv(getPropertyOrDefault("targetEnv", String.class, null, config));
	}


	@Override
	public String getTargetEnv() {
		return targetEnv;
	}
	public void setTargetEnv(String targetEnv) {
		this.targetEnv = targetEnv;
	}

	private <T> T getPropertyOrDefault(String key, Class<T> clazz, T defaultValue, Map<String, Object> config)
			throws ConfigurationException {

		Object object = config.get(key);

		if (object == null) {
			return defaultValue;
		}

		if (clazz.isAssignableFrom(object.getClass())) {
			return clazz.cast(object);
		} else {
			throw new ConfigurationException(key,
					String.format("Expected class '%s', but was '%s'", clazz.getName(), object.getClass().getName()));
		}
	}
	
}
