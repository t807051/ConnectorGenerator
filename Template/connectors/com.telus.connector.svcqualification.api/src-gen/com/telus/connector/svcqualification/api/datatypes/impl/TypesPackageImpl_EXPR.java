package com.telus.connector.svcqualification.api.datatypes.impl;
import com.telus.connector.svcqualification.api.datatypes.Characteristic;
import com.telus.connector.svcqualification.api.datatypes.EligibilityUnavailabilityReason;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationDataRecord;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationEntity;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest;
import com.telus.connector.svcqualification.api.datatypes.Place;
import com.telus.connector.svcqualification.api.datatypes.Service;
import com.telus.connector.svcqualification.api.datatypes.ServiceQualificationItem;
import com.telus.connector.svcqualification.api.datatypes.ServiceSpecification;
import com.telus.connector.svcqualification.api.datatypes.TypesFactory;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import java.util.Collection;
import org.eclipse.emf.ecore.EAttribute;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.EDataType;
import org.eclipse.emf.ecore.EOperation;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.EReference;
import org.eclipse.emf.ecore.impl.EPackageImpl;
public class TypesPackageImpl_EXPR extends EPackageImpl implements TypesPackage
{
	private EClass getSvcQualificationRequestEClass = null;
	private EClass getSvcQualificationDataRecordEClass = null;
	private EClass getSvcQualificationEntityEClass = null;
	private EClass serviceQualificationItemEClass = null;
	private EClass serviceSpecificationEClass = null;
	private EClass serviceEClass = null;
	private EClass characteristicEClass = null;
	private EClass placeEClass = null;
	private EClass eligibilityUnavailabilityReasonEClass = null;
	private EDataType __Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItemEDataType = null;
	private EDataType __Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_CharacteristicEDataType = null;
	private EDataType __Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_PlaceEDataType = null;
	private EDataType __Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReasonEDataType = null;
	private TypesPackageImpl_EXPR()
	{
		super(eNS_URI, TypesFactory.eINSTANCE);
	}
	private static boolean isInited = false;
	public static TypesPackage init()
	{
		if (isInited) return (TypesPackage)EPackage.Registry.INSTANCE.getEPackage(TypesPackage.eNS_URI);
		// Obtain or create and register package
		Object registeredTypesPackage = EPackage.Registry.INSTANCE.get(eNS_URI);
		TypesPackageImpl_EXPR theTypesPackage = registeredTypesPackage instanceof TypesPackageImpl_EXPR ? (TypesPackageImpl_EXPR)registeredTypesPackage : new TypesPackageImpl_EXPR();
		isInited = true;
		// Initialize simple dependencies
		com.iisy.solvatio.domain.EntityModelPackage.eINSTANCE.eClass();
		com.telus.common.api.datatypes.TypesPackage.eINSTANCE.eClass();
		// Create package meta-data objects
		theTypesPackage.createPackageContents();
		// Initialize created meta-data
		theTypesPackage.initializePackageContents();
		// Mark meta-data to indicate it can't be changed
		theTypesPackage.freeze();
		// Update the registry and return the package
		EPackage.Registry.INSTANCE.put(TypesPackage.eNS_URI, theTypesPackage);
		return theTypesPackage;
	}
	@Override
	public EClass getGetSvcQualificationRequest()
	{
		return getSvcQualificationRequestEClass;
	}
	@Override
	public EAttribute getGetSvcQualificationRequest_LpdsId()
	{
		return (EAttribute)getSvcQualificationRequestEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EClass getGetSvcQualificationDataRecord()
	{
		return getSvcQualificationDataRecordEClass;
	}
	@Override
	public EReference getGetSvcQualificationDataRecord_SvcQualificationEntity()
	{
		return (EReference)getSvcQualificationDataRecordEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EClass getGetSvcQualificationEntity()
	{
		return getSvcQualificationEntityEClass;
	}
	@Override
	public EAttribute getGetSvcQualificationEntity_Id()
	{
		return (EAttribute)getSvcQualificationEntityEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EAttribute getGetSvcQualificationEntity_QualificationResult()
	{
		return (EAttribute)getSvcQualificationEntityEClass.getEStructuralFeatures().get(1);
	}
	@Override
	public EAttribute getGetSvcQualificationEntity_ExternalId()
	{
		return (EAttribute)getSvcQualificationEntityEClass.getEStructuralFeatures().get(2);
	}
	@Override
	public EAttribute getGetSvcQualificationEntity_Description()
	{
		return (EAttribute)getSvcQualificationEntityEClass.getEStructuralFeatures().get(3);
	}
	@Override
	public EReference getGetSvcQualificationEntity_ServiceQualificationItem()
	{
		return (EReference)getSvcQualificationEntityEClass.getEStructuralFeatures().get(4);
	}
	@Override
	public EClass getServiceQualificationItem()
	{
		return serviceQualificationItemEClass;
	}
	@Override
	public EAttribute getServiceQualificationItem_Id()
	{
		return (EAttribute)serviceQualificationItemEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EAttribute getServiceQualificationItem_QualificationResult()
	{
		return (EAttribute)serviceQualificationItemEClass.getEStructuralFeatures().get(1);
	}
	@Override
	public EAttribute getServiceQualificationItem_ExpectedServiceAvailabilityDate()
	{
		return (EAttribute)serviceQualificationItemEClass.getEStructuralFeatures().get(2);
	}
	@Override
	public EReference getServiceQualificationItem_ServiceSpecification()
	{
		return (EReference)serviceQualificationItemEClass.getEStructuralFeatures().get(3);
	}
	@Override
	public EReference getServiceQualificationItem_Service()
	{
		return (EReference)serviceQualificationItemEClass.getEStructuralFeatures().get(4);
	}
	@Override
	public EClass getServiceSpecification()
	{
		return serviceSpecificationEClass;
	}
	@Override
	public EAttribute getServiceSpecification_Name()
	{
		return (EAttribute)serviceSpecificationEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EClass getService()
	{
		return serviceEClass;
	}
	@Override
	public EReference getService_Characteristic()
	{
		return (EReference)serviceEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EReference getService_Place()
	{
		return (EReference)serviceEClass.getEStructuralFeatures().get(1);
	}
	@Override
	public EReference getService_EligibilityUnavailabilityReason()
	{
		return (EReference)serviceEClass.getEStructuralFeatures().get(2);
	}
	@Override
	public EClass getCharacteristic()
	{
		return characteristicEClass;
	}
	@Override
	public EAttribute getCharacteristic_Name()
	{
		return (EAttribute)characteristicEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EAttribute getCharacteristic_Value()
	{
		return (EAttribute)characteristicEClass.getEStructuralFeatures().get(1);
	}
	@Override
	public EClass getPlace()
	{
		return placeEClass;
	}
	@Override
	public EAttribute getPlace_Role()
	{
		return (EAttribute)placeEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EAttribute getPlace_Id()
	{
		return (EAttribute)placeEClass.getEStructuralFeatures().get(1);
	}
	@Override
	public EClass getEligibilityUnavailabilityReason()
	{
		return eligibilityUnavailabilityReasonEClass;
	}
	@Override
	public EAttribute getEligibilityUnavailabilityReason_Label()
	{
		return (EAttribute)eligibilityUnavailabilityReasonEClass.getEStructuralFeatures().get(0);
	}
	@Override
	public EAttribute getEligibilityUnavailabilityReason_Code()
	{
		return (EAttribute)eligibilityUnavailabilityReasonEClass.getEStructuralFeatures().get(1);
	}
	@Override
	public EDataType get__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItem()
	{
		return __Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItemEDataType;
	}
	@Override
	public EDataType get__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_Characteristic()
	{
		return __Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_CharacteristicEDataType;
	}
	@Override
	public EDataType get__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_Place()
	{
		return __Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_PlaceEDataType;
	}
	@Override
	public EDataType get__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReason()
	{
		return __Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReasonEDataType;
	}
	@Override
	public TypesFactory getTypesFactory()
	{
		return (TypesFactory)getEFactoryInstance();
	}
	private boolean isCreated = false;
	public void createPackageContents()
	{
		if (isCreated) return;
		isCreated = true;
		// Create classes and their features
		getSvcQualificationRequestEClass = createEClass(GET_SVC_QUALIFICATION_REQUEST);
		createEAttribute(getSvcQualificationRequestEClass, GET_SVC_QUALIFICATION_REQUEST__LPDS_ID);
		getSvcQualificationDataRecordEClass = createEClass(GET_SVC_QUALIFICATION_DATA_RECORD);
		createEReference(getSvcQualificationDataRecordEClass, GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY);
		getSvcQualificationEntityEClass = createEClass(GET_SVC_QUALIFICATION_ENTITY);
		createEAttribute(getSvcQualificationEntityEClass, GET_SVC_QUALIFICATION_ENTITY__ID);
		createEAttribute(getSvcQualificationEntityEClass, GET_SVC_QUALIFICATION_ENTITY__QUALIFICATION_RESULT);
		createEAttribute(getSvcQualificationEntityEClass, GET_SVC_QUALIFICATION_ENTITY__EXTERNAL_ID);
		createEAttribute(getSvcQualificationEntityEClass, GET_SVC_QUALIFICATION_ENTITY__DESCRIPTION);
		createEReference(getSvcQualificationEntityEClass, GET_SVC_QUALIFICATION_ENTITY__SERVICE_QUALIFICATION_ITEM);
		serviceQualificationItemEClass = createEClass(SERVICE_QUALIFICATION_ITEM);
		createEAttribute(serviceQualificationItemEClass, SERVICE_QUALIFICATION_ITEM__ID);
		createEAttribute(serviceQualificationItemEClass, SERVICE_QUALIFICATION_ITEM__QUALIFICATION_RESULT);
		createEAttribute(serviceQualificationItemEClass, SERVICE_QUALIFICATION_ITEM__EXPECTED_SERVICE_AVAILABILITY_DATE);
		createEReference(serviceQualificationItemEClass, SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION);
		createEReference(serviceQualificationItemEClass, SERVICE_QUALIFICATION_ITEM__SERVICE);
		serviceSpecificationEClass = createEClass(SERVICE_SPECIFICATION);
		createEAttribute(serviceSpecificationEClass, SERVICE_SPECIFICATION__NAME);
		serviceEClass = createEClass(SERVICE);
		createEReference(serviceEClass, SERVICE__CHARACTERISTIC);
		createEReference(serviceEClass, SERVICE__PLACE);
		createEReference(serviceEClass, SERVICE__ELIGIBILITY_UNAVAILABILITY_REASON);
		characteristicEClass = createEClass(CHARACTERISTIC);
		createEAttribute(characteristicEClass, CHARACTERISTIC__NAME);
		createEAttribute(characteristicEClass, CHARACTERISTIC__VALUE);
		placeEClass = createEClass(PLACE);
		createEAttribute(placeEClass, PLACE__ROLE);
		createEAttribute(placeEClass, PLACE__ID);
		eligibilityUnavailabilityReasonEClass = createEClass(ELIGIBILITY_UNAVAILABILITY_REASON);
		createEAttribute(eligibilityUnavailabilityReasonEClass, ELIGIBILITY_UNAVAILABILITY_REASON__LABEL);
		createEAttribute(eligibilityUnavailabilityReasonEClass, ELIGIBILITY_UNAVAILABILITY_REASON__CODE);
		// Create data types
		__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItemEDataType = createEDataType(_COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_SERVICE_QUALIFICATION_ITEM);
		__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_CharacteristicEDataType = createEDataType(_COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_CHARACTERISTIC);
		__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_PlaceEDataType = createEDataType(_COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_PLACE);
		__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReasonEDataType = createEDataType(_COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_ELIGIBILITY_UNAVAILABILITY_REASON);
	}
	private boolean isInitialized = false;
	public void initializePackageContents()
	{
		if (isInitialized) return;
		isInitialized = true;
		// Initialize package
		setName(eNAME);
		setNsPrefix(eNS_PREFIX);
		setNsURI(eNS_URI);
		// Obtain other dependent packages
		com.iisy.solvatio.domain.EntityModelPackage theEntityModelPackage = (com.iisy.solvatio.domain.EntityModelPackage)EPackage.Registry.INSTANCE.getEPackage(com.iisy.solvatio.domain.util.EntityHelper.getNamespaceURI(com.iisy.solvatio.domain.EntityModelPackage.class));
		com.telus.common.api.datatypes.TypesPackage theTypesPackage_1 = (com.telus.common.api.datatypes.TypesPackage)EPackage.Registry.INSTANCE.getEPackage(com.iisy.solvatio.domain.util.EntityHelper.getNamespaceURI(com.telus.common.api.datatypes.TypesPackage.class));
		// Create type parameters
		// Set bounds for type parameters
		// Add supertypes to classes
		getSvcQualificationRequestEClass.getESuperTypes().add(theEntityModelPackage.getBaseStruct());
		getSvcQualificationDataRecordEClass.getESuperTypes().add(theTypesPackage_1.getAbstractDataRecord());
		getSvcQualificationEntityEClass.getESuperTypes().add(theEntityModelPackage.getBaseStruct());
		serviceQualificationItemEClass.getESuperTypes().add(theEntityModelPackage.getBaseStruct());
		serviceSpecificationEClass.getESuperTypes().add(theEntityModelPackage.getBaseStruct());
		serviceEClass.getESuperTypes().add(theEntityModelPackage.getBaseStruct());
		characteristicEClass.getESuperTypes().add(theEntityModelPackage.getBaseStruct());
		placeEClass.getESuperTypes().add(theEntityModelPackage.getBaseStruct());
		eligibilityUnavailabilityReasonEClass.getESuperTypes().add(theEntityModelPackage.getBaseStruct());
		// Initialize classes and features; add operations and parameters
		initEClass(getSvcQualificationRequestEClass, GetSvcQualificationRequest.class, "GetSvcQualificationRequest", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEAttribute(getGetSvcQualificationRequest_LpdsId(), ecorePackage.getEString(), "lpdsId", null, 0, 1, GetSvcQualificationRequest.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEClass(getSvcQualificationDataRecordEClass, GetSvcQualificationDataRecord.class, "GetSvcQualificationDataRecord", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEReference(getGetSvcQualificationDataRecord_SvcQualificationEntity(), this.getGetSvcQualificationEntity(), null, "svcQualificationEntity", null, 0, 1, GetSvcQualificationDataRecord.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, IS_COMPOSITE, IS_RESOLVE_PROXIES, !IS_UNSETTABLE, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEClass(getSvcQualificationEntityEClass, GetSvcQualificationEntity.class, "GetSvcQualificationEntity", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEAttribute(getGetSvcQualificationEntity_Id(), ecorePackage.getEString(), "id", null, 0, 1, GetSvcQualificationEntity.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEAttribute(getGetSvcQualificationEntity_QualificationResult(), ecorePackage.getEString(), "qualificationResult", null, 0, 1, GetSvcQualificationEntity.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEAttribute(getGetSvcQualificationEntity_ExternalId(), ecorePackage.getEString(), "externalId", null, 0, 1, GetSvcQualificationEntity.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEAttribute(getGetSvcQualificationEntity_Description(), ecorePackage.getEString(), "description", null, 0, 1, GetSvcQualificationEntity.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEReference(getGetSvcQualificationEntity_ServiceQualificationItem(), this.getServiceQualificationItem(), null, "serviceQualificationItem", null, 0, -1, GetSvcQualificationEntity.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, IS_COMPOSITE, IS_RESOLVE_PROXIES, !IS_UNSETTABLE, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		EOperation op = addEOperation(getSvcQualificationEntityEClass, null, "setServiceQualificationItem", 0, 1, !IS_UNIQUE, IS_ORDERED);
		addEParameter(op, this.get__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItem(), "value", 0, 1, IS_UNIQUE, IS_ORDERED);
		initEClass(serviceQualificationItemEClass, ServiceQualificationItem.class, "ServiceQualificationItem", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEAttribute(getServiceQualificationItem_Id(), ecorePackage.getEString(), "id", null, 0, 1, ServiceQualificationItem.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEAttribute(getServiceQualificationItem_QualificationResult(), ecorePackage.getEString(), "qualificationResult", null, 0, 1, ServiceQualificationItem.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEAttribute(getServiceQualificationItem_ExpectedServiceAvailabilityDate(), ecorePackage.getEString(), "expectedServiceAvailabilityDate", null, 0, 1, ServiceQualificationItem.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEReference(getServiceQualificationItem_ServiceSpecification(), this.getServiceSpecification(), null, "serviceSpecification", null, 0, 1, ServiceQualificationItem.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, IS_COMPOSITE, IS_RESOLVE_PROXIES, !IS_UNSETTABLE, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEReference(getServiceQualificationItem_Service(), this.getService(), null, "service", null, 0, 1, ServiceQualificationItem.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, IS_COMPOSITE, IS_RESOLVE_PROXIES, !IS_UNSETTABLE, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEClass(serviceSpecificationEClass, ServiceSpecification.class, "ServiceSpecification", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEAttribute(getServiceSpecification_Name(), ecorePackage.getEString(), "name", null, 0, 1, ServiceSpecification.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEClass(serviceEClass, Service.class, "Service", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEReference(getService_Characteristic(), this.getCharacteristic(), null, "characteristic", null, 0, -1, Service.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, IS_COMPOSITE, IS_RESOLVE_PROXIES, !IS_UNSETTABLE, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEReference(getService_Place(), this.getPlace(), null, "place", null, 0, -1, Service.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, IS_COMPOSITE, IS_RESOLVE_PROXIES, !IS_UNSETTABLE, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEReference(getService_EligibilityUnavailabilityReason(), this.getEligibilityUnavailabilityReason(), null, "eligibilityUnavailabilityReason", null, 0, -1, Service.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, IS_COMPOSITE, IS_RESOLVE_PROXIES, !IS_UNSETTABLE, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		op = addEOperation(serviceEClass, null, "setCharacteristic", 0, 1, !IS_UNIQUE, IS_ORDERED);
		addEParameter(op, this.get__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_Characteristic(), "value", 0, 1, IS_UNIQUE, IS_ORDERED);
		op = addEOperation(serviceEClass, null, "setPlace", 0, 1, !IS_UNIQUE, IS_ORDERED);
		addEParameter(op, this.get__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_Place(), "value", 0, 1, IS_UNIQUE, IS_ORDERED);
		op = addEOperation(serviceEClass, null, "setEligibilityUnavailabilityReason", 0, 1, !IS_UNIQUE, IS_ORDERED);
		addEParameter(op, this.get__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReason(), "value", 0, 1, IS_UNIQUE, IS_ORDERED);
		initEClass(characteristicEClass, Characteristic.class, "Characteristic", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEAttribute(getCharacteristic_Name(), ecorePackage.getEString(), "name", null, 0, 1, Characteristic.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEAttribute(getCharacteristic_Value(), ecorePackage.getEString(), "value", null, 0, 1, Characteristic.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEClass(placeEClass, Place.class, "Place", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEAttribute(getPlace_Role(), ecorePackage.getEString(), "role", null, 0, 1, Place.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEAttribute(getPlace_Id(), ecorePackage.getEString(), "id", null, 0, 1, Place.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEClass(eligibilityUnavailabilityReasonEClass, EligibilityUnavailabilityReason.class, "EligibilityUnavailabilityReason", !IS_ABSTRACT, !IS_INTERFACE, IS_GENERATED_INSTANCE_CLASS);
		initEAttribute(getEligibilityUnavailabilityReason_Label(), ecorePackage.getEString(), "label", null, 0, 1, EligibilityUnavailabilityReason.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		initEAttribute(getEligibilityUnavailabilityReason_Code(), ecorePackage.getEIntegerObject(), "code", null, 0, 1, EligibilityUnavailabilityReason.class, !IS_TRANSIENT, !IS_VOLATILE, IS_CHANGEABLE, !IS_UNSETTABLE, !IS_ID, !IS_UNIQUE, !IS_DERIVED, IS_ORDERED);
		// Initialize data types
		initEDataType(__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItemEDataType, Collection.class, "__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItem", IS_SERIALIZABLE, !IS_GENERATED_INSTANCE_CLASS, "java.util.Collection<? extends com.telus.connector.svcqualification.api.datatypes.ServiceQualificationItem>");
		initEDataType(__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_CharacteristicEDataType, Collection.class, "__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_Characteristic", IS_SERIALIZABLE, !IS_GENERATED_INSTANCE_CLASS, "java.util.Collection<? extends com.telus.connector.svcqualification.api.datatypes.Characteristic>");
		initEDataType(__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_PlaceEDataType, Collection.class, "__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_Place", IS_SERIALIZABLE, !IS_GENERATED_INSTANCE_CLASS, "java.util.Collection<? extends com.telus.connector.svcqualification.api.datatypes.Place>");
		initEDataType(__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReasonEDataType, Collection.class, "__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReason", IS_SERIALIZABLE, !IS_GENERATED_INSTANCE_CLASS, "java.util.Collection<? extends com.telus.connector.svcqualification.api.datatypes.EligibilityUnavailabilityReason>");
		// Create resource
		createResource(eNS_URI);
		// Create annotations
		// solvatio.studio.property
		createSolvatioAnnotations();
	}
	protected void createSolvatioAnnotations()
	{
		String source = "solvatio.studio.property";
		addAnnotation
		  (getSvcQualificationEntityEClass.getEOperations().get(0),
		   source,
		   new String[]
		   {
			   "name", "serviceQualificationItem"
		   });
		addAnnotation
		  (serviceEClass.getEOperations().get(0),
		   source,
		   new String[]
		   {
			   "name", "characteristic"
		   });
		addAnnotation
		  (serviceEClass.getEOperations().get(1),
		   source,
		   new String[]
		   {
			   "name", "place"
		   });
		addAnnotation
		  (serviceEClass.getEOperations().get(2),
		   source,
		   new String[]
		   {
			   "name", "eligibilityUnavailabilityReason"
		   });
	}
} //TypesPackageImpl_EXPR