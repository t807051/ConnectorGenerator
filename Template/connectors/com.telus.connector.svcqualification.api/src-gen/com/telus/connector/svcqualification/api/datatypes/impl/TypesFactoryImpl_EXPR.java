package com.telus.connector.svcqualification.api.datatypes.impl;
import com.telus.connector.svcqualification.api.datatypes.*;
import java.util.Collection;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.EDataType;
import org.eclipse.emf.ecore.EObject;
import org.eclipse.emf.ecore.EPackage;
import org.eclipse.emf.ecore.impl.EFactoryImpl;
import org.eclipse.emf.ecore.plugin.EcorePlugin;
public class TypesFactoryImpl_EXPR extends EFactoryImpl implements TypesFactory
{
	public static TypesFactory init()
	{
		try
		{
			TypesFactory theTypesFactory = (TypesFactory)EPackage.Registry.INSTANCE.getEFactory(TypesPackage.eNS_URI);
			if (theTypesFactory != null)
			{
				return theTypesFactory;
			}
		}
		catch (Exception exception)
		{
			EcorePlugin.INSTANCE.log(exception);
		}
		return new TypesFactoryImpl_EXPR();
	}
	public TypesFactoryImpl_EXPR()
	{
		super();
	}
	@Override
	public EObject create(EClass eClass)
	{
		switch (eClass.getClassifierID())
		{
			case TypesPackage.GET_SVC_QUALIFICATION_REQUEST: return (EObject) createGetSvcQualificationRequest();
			case TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD: return (EObject) createGetSvcQualificationDataRecord();
			case TypesPackage.GET_SVC_QUALIFICATION_ENTITY: return (EObject) createGetSvcQualificationEntity();
			case TypesPackage.SERVICE_QUALIFICATION_ITEM: return (EObject) createServiceQualificationItem();
			case TypesPackage.SERVICE_SPECIFICATION: return (EObject) createServiceSpecification();
			case TypesPackage.SERVICE: return (EObject) createService();
			case TypesPackage.CHARACTERISTIC: return (EObject) createCharacteristic();
			case TypesPackage.PLACE: return (EObject) createPlace();
			case TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON: return (EObject) createEligibilityUnavailabilityReason();
			default:
				throw new IllegalArgumentException("The class '" + eClass.getName() + "' is not a valid classifier");
		}
	}
	@Override
	public Object createFromString(EDataType eDataType, String initialValue)
	{
		switch (eDataType.getClassifierID())
		{
			case TypesPackage._COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_SERVICE_QUALIFICATION_ITEM:
				return create__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItemFromString(eDataType, initialValue);
			case TypesPackage._COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_CHARACTERISTIC:
				return create__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_CharacteristicFromString(eDataType, initialValue);
			case TypesPackage._COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_PLACE:
				return create__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_PlaceFromString(eDataType, initialValue);
			case TypesPackage._COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_ELIGIBILITY_UNAVAILABILITY_REASON:
				return create__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReasonFromString(eDataType, initialValue);
			default:
				throw new IllegalArgumentException("The datatype '" + eDataType.getName() + "' is not a valid classifier");
		}
	}
	@Override
	public String convertToString(EDataType eDataType, Object instanceValue)
	{
		switch (eDataType.getClassifierID())
		{
			case TypesPackage._COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_SERVICE_QUALIFICATION_ITEM:
				return convert__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItemToString(eDataType, instanceValue);
			case TypesPackage._COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_CHARACTERISTIC:
				return convert__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_CharacteristicToString(eDataType, instanceValue);
			case TypesPackage._COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_PLACE:
				return convert__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_PlaceToString(eDataType, instanceValue);
			case TypesPackage._COLLECTION_DATATYPES_COM_TELUS_CONNECTOR_SVCQUALIFICATION_API_DATATYPES_ELIGIBILITY_UNAVAILABILITY_REASON:
				return convert__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReasonToString(eDataType, instanceValue);
			default:
				throw new IllegalArgumentException("The datatype '" + eDataType.getName() + "' is not a valid classifier");
		}
	}
	@Override
	public GetSvcQualificationRequest createGetSvcQualificationRequest()
	{
		GetSvcQualificationRequestImpl_EXPR getSvcQualificationRequest = new GetSvcQualificationRequestImpl_EXPR();
		return getSvcQualificationRequest;
	}
	@Override
	public GetSvcQualificationDataRecord createGetSvcQualificationDataRecord()
	{
		GetSvcQualificationDataRecordImpl_EXPR getSvcQualificationDataRecord = new GetSvcQualificationDataRecordImpl_EXPR();
		return getSvcQualificationDataRecord;
	}
	@Override
	public GetSvcQualificationEntity createGetSvcQualificationEntity()
	{
		GetSvcQualificationEntityImpl_EXPR getSvcQualificationEntity = new GetSvcQualificationEntityImpl_EXPR();
		return getSvcQualificationEntity;
	}
	@Override
	public ServiceQualificationItem createServiceQualificationItem()
	{
		ServiceQualificationItemImpl_EXPR serviceQualificationItem = new ServiceQualificationItemImpl_EXPR();
		return serviceQualificationItem;
	}
	@Override
	public ServiceSpecification createServiceSpecification()
	{
		ServiceSpecificationImpl_EXPR serviceSpecification = new ServiceSpecificationImpl_EXPR();
		return serviceSpecification;
	}
	@Override
	public Service createService()
	{
		ServiceImpl_EXPR service = new ServiceImpl_EXPR();
		return service;
	}
	@Override
	public Characteristic createCharacteristic()
	{
		CharacteristicImpl_EXPR characteristic = new CharacteristicImpl_EXPR();
		return characteristic;
	}
	@Override
	public Place createPlace()
	{
		PlaceImpl_EXPR place = new PlaceImpl_EXPR();
		return place;
	}
	@Override
	public EligibilityUnavailabilityReason createEligibilityUnavailabilityReason()
	{
		EligibilityUnavailabilityReasonImpl_EXPR eligibilityUnavailabilityReason = new EligibilityUnavailabilityReasonImpl_EXPR();
		return eligibilityUnavailabilityReason;
	}
	@SuppressWarnings("unchecked")
	public Collection<? extends ServiceQualificationItem> create__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItemFromString(EDataType eDataType, String initialValue)
	{
		return (Collection<? extends ServiceQualificationItem>)super.createFromString(initialValue);
	}
	public String convert__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_ServiceQualificationItemToString(EDataType eDataType, Object instanceValue)
	{
		return super.convertToString(instanceValue);
	}
	@SuppressWarnings("unchecked")
	public Collection<? extends Characteristic> create__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_CharacteristicFromString(EDataType eDataType, String initialValue)
	{
		return (Collection<? extends Characteristic>)super.createFromString(initialValue);
	}
	public String convert__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_CharacteristicToString(EDataType eDataType, Object instanceValue)
	{
		return super.convertToString(instanceValue);
	}
	@SuppressWarnings("unchecked")
	public Collection<? extends Place> create__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_PlaceFromString(EDataType eDataType, String initialValue)
	{
		return (Collection<? extends Place>)super.createFromString(initialValue);
	}
	public String convert__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_PlaceToString(EDataType eDataType, Object instanceValue)
	{
		return super.convertToString(instanceValue);
	}
	@SuppressWarnings("unchecked")
	public Collection<? extends EligibilityUnavailabilityReason> create__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReasonFromString(EDataType eDataType, String initialValue)
	{
		return (Collection<? extends EligibilityUnavailabilityReason>)super.createFromString(initialValue);
	}
	public String convert__Collection__datatypes_com_telus_connector_svcqualification_api_datatypes_EligibilityUnavailabilityReasonToString(EDataType eDataType, Object instanceValue)
	{
		return super.convertToString(instanceValue);
	}
	@Override
	public TypesPackage getTypesPackage()
	{
		return (TypesPackage)getEPackage();
	}
	@Deprecated
	public static TypesPackage getPackage()
	{
		return TypesPackage.eINSTANCE;
	}
} //TypesFactoryImpl_EXPR