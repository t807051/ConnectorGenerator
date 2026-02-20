package com.telus.connector.svcqualification.call;

import java.util.Map;

import javax.ws.rs.client.Entity;
import javax.ws.rs.client.Invocation.Builder;
import javax.ws.rs.client.InvocationCallback;
import javax.ws.rs.client.WebTarget;
import javax.ws.rs.core.MediaType;

import org.slf4j.LoggerFactory;

import com.iisy.solvatio.connector.AsyncConnectorCallback;
import com.iisy.solvatio.connector.ConnectorError;
import com.iisy.solvatio.connector.ConnectorException;
import com.solvatio.connector.rest.common.connector.AsyncRestConnector;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationDataRecord;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationEntity;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest;


public class GetSvcQualificationConnector extends AsyncRestConnector<GetSvcQualificationDataRecord> {
	public static final String ID = "GetSvcQualification";
	public final static String QUALIFIED_ID = "com.telus.connector.svcqualification" + "." + ID;
	public String targetEnv;

	public GetSvcQualificationConnector(WebTarget target) {
		super(target, LoggerFactory.getLogger(QUALIFIED_ID));
	}

	@Override
	public void execute(Map<String, Object> args, AsyncConnectorCallback<GetSvcQualificationDataRecord> callback)
			throws ConnectorException {
		logger.info("Get Service Qualification... ");
		
		GetSvcQualificationRequest request = (GetSvcQualificationRequest) args.get("parameters");
		if ((request == null) || (request.getLpdsId() == null)) {
			logger.error("Missing Parameter : lpdsId. ");
			callback.failed(new ConnectorError("Missing Parameter : lpdsId"));
		}
			


		try {

			Builder requestBuilder = this.target
				.path(request.getLpdsId())
				.request(MediaType.APPLICATION_JSON);
	        
	        if (targetEnv != null && !targetEnv.isEmpty()) {
	            requestBuilder.header("env", this.targetEnv);
	        }

			requestBuilder
				.header("Content-type", MediaType.APPLICATION_JSON)
				.accept(MediaType.APPLICATION_JSON)
				.async().method("GET", Entity.entity(null, MediaType.APPLICATION_JSON_TYPE),
						new InvocationCallback<GetSvcQualificationEntity>() {
							@Override
							public void completed(GetSvcQualificationEntity entity) {
								GetSvcQualificationDataRecord dataRecord = GetSvcQualificationDataRecord.create();
								dataRecord.setSvcQualificationEntity(entity);
								callback.complete(dataRecord);
							}

							@Override
							public void failed(Throwable cause) {
								logger.error("Connector callback failed. ", cause);
								callback.failed(new ConnectorError(cause.getMessage()));
							}

						});

		} catch (Exception cause) {
			logger.error("Connector call failed. ", cause);
			callback.failed(new ConnectorError(cause.getMessage()));
		}

		
	}

}
