package com.telus.connector.svcqualification.api.datatypes;
import org.eclipse.emf.ecore.EFactory;
public interface TypesFactory extends EFactory
{
	TypesFactory eINSTANCE = com.telus.connector.svcqualification.api.datatypes.impl.TypesFactoryImpl_EXPR.init();
	GetSvcQualificationRequest createGetSvcQualificationRequest();
	GetSvcQualificationDataRecord createGetSvcQualificationDataRecord();
	GetSvcQualificationEntity createGetSvcQualificationEntity();
	ServiceQualificationItem createServiceQualificationItem();
	ServiceSpecification createServiceSpecification();
	Service createService();
	Characteristic createCharacteristic();
	Place createPlace();
	EligibilityUnavailabilityReason createEligibilityUnavailabilityReason();
	TypesPackage getTypesPackage();
} //TypesFactory