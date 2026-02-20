package com.telus.connector.svcqualification.factories;

import javax.ws.rs.Priorities;
import javax.ws.rs.client.WebTarget;

import org.osgi.service.component.annotations.Component;
import org.osgi.service.component.annotations.Reference;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.MDC;

import com.fasterxml.jackson.databind.ObjectMapper;
import com.iisy.solvatio.connector.ConnectorException;
import com.iisy.solvatio.connector.ConnectorFactory;
import com.solvatio.connector.rest.common.connector.AsyncRestConnectorFactory;
import com.solvatio.connector.rest.common.domaininterface.json.io.JsonToDomainReader;
import com.solvatio.connector.rest.common.logging.SLF4JRequestFilter;
import com.solvatio.connector.rest.common.logging.SLF4JResponseFilter;
import com.telus.connector.svcqualification.Constants;
import com.telus.connector.svcqualification.ISvcQualificationConfigurationComponent;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationEntity;
import com.telus.connector.svcqualification.call.GetSvcQualificationConnector;
import com.telus.connector.svcqualification.converter.GetSvcQualificationConverter;

@Component(service = ConnectorFactory.class, name = "com.telus.connector.svcqualification.GetSvcQualification"
		+ Constants.VERSION, property = {"connectorId=com.telus.connector.svcqualification.GetSvcQualification",
				"version=" + Constants.VERSION, "type=rest" }, immediate = true)
public class GetSvcQualificationFactory extends AsyncRestConnectorFactory<GetSvcQualificationConnector> {

	public static final String PATH = "/service/serviceQualification/v2/serviceQualification";
	private WebTarget webTarget;
	public String targetEnv;

	@Override
	public GetSvcQualificationConnector createConnector() throws ConnectorException {
		String caseId = MDC.get("caseId");
		String correlationId = MDC.get("correlationId");
		String configuredUri = null;
		try {
			configuredUri = this.webTarget.getUri().toString();
		} catch (Exception e) {
		}
		WebTarget webTargetWithLogging = this.webTarget.path("")
				.register(new SLF4JRequestFilter(caseId, correlationId, configuredUri,
						GetSvcQualificationConnector.class), Priorities.USER)
				.register(new SLF4JResponseFilter(caseId, correlationId, GetSvcQualificationConnector.class),
						Priorities.USER);
		GetSvcQualificationConnector connector = new GetSvcQualificationConnector(webTargetWithLogging);
		connector.targetEnv = this.targetEnv;
		return connector;
	}

	@Reference(target = "(target=com.telus.connector.svcqualification.SvcQualification)")
	public void bindConfigurationComponent(final ISvcQualificationConfigurationComponent component) {
		this.configuration = component;
		this.webTarget = component.getWebTarget().path(PATH);
		Logger logger = LoggerFactory.getLogger(GetSvcQualificationConnector.QUALIFIED_ID);
		ObjectMapper objectMapper = new ObjectMapper();
		final JsonToDomainReader<GetSvcQualificationEntity> jsonToDomainReader = new JsonToDomainReader<>(
				new GetSvcQualificationConverter(), objectMapper, logger);
		this.webTarget = webTarget.register(jsonToDomainReader);
		this.targetEnv = component.getTargetEnv();
	}

	public void unbindConfigurationComponent(final ISvcQualificationConfigurationComponent component) {
		this.configuration = null;
	}

}
