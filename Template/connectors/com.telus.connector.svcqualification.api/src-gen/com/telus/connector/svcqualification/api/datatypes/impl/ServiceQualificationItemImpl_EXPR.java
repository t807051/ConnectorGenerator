package com.telus.connector.svcqualification.api.datatypes.impl;
import com.iisy.solvatio.domain.impl.BaseStructImpl;
import com.telus.connector.svcqualification.api.datatypes.Service;
import com.telus.connector.svcqualification.api.datatypes.ServiceQualificationItem;
import com.telus.connector.svcqualification.api.datatypes.ServiceSpecification;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.emf.common.notify.NotificationChain;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.InternalEObject;
import org.eclipse.emf.ecore.impl.ENotificationImpl;
public class ServiceQualificationItemImpl_EXPR extends BaseStructImpl implements ServiceQualificationItem
{
	private static final long serialVersionUID = 1L;
	protected static final String ID_EDEFAULT = null;
	protected String id = ID_EDEFAULT;
	protected static final String QUALIFICATION_RESULT_EDEFAULT = null;
	protected String qualificationResult = QUALIFICATION_RESULT_EDEFAULT;
	protected static final String EXPECTED_SERVICE_AVAILABILITY_DATE_EDEFAULT = null;
	protected String expectedServiceAvailabilityDate = EXPECTED_SERVICE_AVAILABILITY_DATE_EDEFAULT;
	protected ServiceSpecification serviceSpecification;
	protected Service service;
	public ServiceQualificationItemImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.ServiceQualificationItem";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getServiceQualificationItem();
	}
	@Override
	public String getId()
	{
		return id;
	}
	@Override
	public void setId(String newId)
	{
		newId = processNewValue(id, newId);
		String oldId = id;
		id = newId;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.SERVICE_QUALIFICATION_ITEM__ID, oldId, id));
	}
	@Override
	public String getQualificationResult()
	{
		return qualificationResult;
	}
	@Override
	public void setQualificationResult(String newQualificationResult)
	{
		newQualificationResult = processNewValue(qualificationResult, newQualificationResult);
		String oldQualificationResult = qualificationResult;
		qualificationResult = newQualificationResult;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.SERVICE_QUALIFICATION_ITEM__QUALIFICATION_RESULT, oldQualificationResult, qualificationResult));
	}
	@Override
	public String getExpectedServiceAvailabilityDate()
	{
		return expectedServiceAvailabilityDate;
	}
	@Override
	public void setExpectedServiceAvailabilityDate(String newExpectedServiceAvailabilityDate)
	{
		newExpectedServiceAvailabilityDate = processNewValue(expectedServiceAvailabilityDate, newExpectedServiceAvailabilityDate);
		String oldExpectedServiceAvailabilityDate = expectedServiceAvailabilityDate;
		expectedServiceAvailabilityDate = newExpectedServiceAvailabilityDate;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.SERVICE_QUALIFICATION_ITEM__EXPECTED_SERVICE_AVAILABILITY_DATE, oldExpectedServiceAvailabilityDate, expectedServiceAvailabilityDate));
	}
	@Override
	public ServiceSpecification getServiceSpecification()
	{
		if (serviceSpecification != null && ((InternalEObject) serviceSpecification).eIsProxy())
		{
			InternalEObject oldServiceSpecification = (InternalEObject)serviceSpecification;
			serviceSpecification = (ServiceSpecification)eResolveProxy(oldServiceSpecification);
			if (serviceSpecification != oldServiceSpecification)
			{
				InternalEObject newServiceSpecification = (InternalEObject)serviceSpecification;
				NotificationChain msgs = oldServiceSpecification.eInverseRemove(this, EOPPOSITE_FEATURE_BASE - TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION, null, null);
				if (newServiceSpecification.eInternalContainer() == null)
				{
					msgs = newServiceSpecification.eInverseAdd(this, EOPPOSITE_FEATURE_BASE - TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION, null, msgs);
				}
				if (msgs != null) msgs.dispatch();
				if (eNotificationRequired())
					eNotify(new ENotificationImpl(this, Notification.RESOLVE, TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION, oldServiceSpecification, serviceSpecification));
			}
		}
		return serviceSpecification;
	}
	public ServiceSpecification basicGetServiceSpecification()
	{
		return serviceSpecification;
	}
	public NotificationChain basicSetServiceSpecification(ServiceSpecification newServiceSpecification, NotificationChain msgs)
	{
		ServiceSpecification oldServiceSpecification = serviceSpecification;
		serviceSpecification = newServiceSpecification;
		if (eNotificationRequired())
		{
			ENotificationImpl notification = new ENotificationImpl(this, Notification.SET, TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION, oldServiceSpecification, newServiceSpecification);
			if (msgs == null) msgs = notification; else msgs.add(notification);
		}
		return msgs;
	}
	@Override
	public void setServiceSpecification(ServiceSpecification newServiceSpecification)
	{
		newServiceSpecification = processNewValue(serviceSpecification, newServiceSpecification);
		if (newServiceSpecification != serviceSpecification)
		{
			NotificationChain msgs = null;
			if (serviceSpecification != null)
				msgs = ((InternalEObject)serviceSpecification).eInverseRemove(this, EOPPOSITE_FEATURE_BASE - TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION, null, msgs);
			if (newServiceSpecification != null)
				msgs = ((InternalEObject)newServiceSpecification).eInverseAdd(this, EOPPOSITE_FEATURE_BASE - TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION, null, msgs);
			msgs = basicSetServiceSpecification(newServiceSpecification, msgs);
			if (msgs != null) msgs.dispatch();
		}
		else if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION, newServiceSpecification, newServiceSpecification));
	}
	@Override
	public Service getService()
	{
		if (service != null && ((InternalEObject) service).eIsProxy())
		{
			InternalEObject oldService = (InternalEObject)service;
			service = (Service)eResolveProxy(oldService);
			if (service != oldService)
			{
				InternalEObject newService = (InternalEObject)service;
				NotificationChain msgs = oldService.eInverseRemove(this, EOPPOSITE_FEATURE_BASE - TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE, null, null);
				if (newService.eInternalContainer() == null)
				{
					msgs = newService.eInverseAdd(this, EOPPOSITE_FEATURE_BASE - TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE, null, msgs);
				}
				if (msgs != null) msgs.dispatch();
				if (eNotificationRequired())
					eNotify(new ENotificationImpl(this, Notification.RESOLVE, TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE, oldService, service));
			}
		}
		return service;
	}
	public Service basicGetService()
	{
		return service;
	}
	public NotificationChain basicSetService(Service newService, NotificationChain msgs)
	{
		Service oldService = service;
		service = newService;
		if (eNotificationRequired())
		{
			ENotificationImpl notification = new ENotificationImpl(this, Notification.SET, TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE, oldService, newService);
			if (msgs == null) msgs = notification; else msgs.add(notification);
		}
		return msgs;
	}
	@Override
	public void setService(Service newService)
	{
		newService = processNewValue(service, newService);
		if (newService != service)
		{
			NotificationChain msgs = null;
			if (service != null)
				msgs = ((InternalEObject)service).eInverseRemove(this, EOPPOSITE_FEATURE_BASE - TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE, null, msgs);
			if (newService != null)
				msgs = ((InternalEObject)newService).eInverseAdd(this, EOPPOSITE_FEATURE_BASE - TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE, null, msgs);
			msgs = basicSetService(newService, msgs);
			if (msgs != null) msgs.dispatch();
		}
		else if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE, newService, newService));
	}
	@Override
	public NotificationChain eInverseRemove(InternalEObject otherEnd, int featureID, NotificationChain msgs)
	{
		if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION)
		{
			return basicSetServiceSpecification(null, msgs);
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE)
		{
			return basicSetService(null, msgs);
		}
		return super.eInverseRemove(otherEnd, featureID, msgs);
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__ID)
		{
			return getId();
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__QUALIFICATION_RESULT)
		{
			return getQualificationResult();
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__EXPECTED_SERVICE_AVAILABILITY_DATE)
		{
			return getExpectedServiceAvailabilityDate();
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION)
		{
			if (resolve) return getServiceSpecification();
			return basicGetServiceSpecification();
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE)
		{
			if (resolve) return getService();
			return basicGetService();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__ID)
		{
			setId((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__QUALIFICATION_RESULT)
		{
			setQualificationResult((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__EXPECTED_SERVICE_AVAILABILITY_DATE)
		{
			setExpectedServiceAvailabilityDate((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION)
		{
			setServiceSpecification((ServiceSpecification)newValue);
			return;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE)
		{
			setService((Service)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__ID)
		{
			setId(ID_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__QUALIFICATION_RESULT)
		{
			setQualificationResult(QUALIFICATION_RESULT_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__EXPECTED_SERVICE_AVAILABILITY_DATE)
		{
			setExpectedServiceAvailabilityDate(EXPECTED_SERVICE_AVAILABILITY_DATE_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION)
		{
			setServiceSpecification((ServiceSpecification)null);
			return;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE)
		{
			setService((Service)null);
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__ID)
		{
			return ID_EDEFAULT == null ? id != null : !ID_EDEFAULT.equals(id);
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__QUALIFICATION_RESULT)
		{
			return QUALIFICATION_RESULT_EDEFAULT == null ? qualificationResult != null : !QUALIFICATION_RESULT_EDEFAULT.equals(qualificationResult);
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__EXPECTED_SERVICE_AVAILABILITY_DATE)
		{
			return EXPECTED_SERVICE_AVAILABILITY_DATE_EDEFAULT == null ? expectedServiceAvailabilityDate != null : !EXPECTED_SERVICE_AVAILABILITY_DATE_EDEFAULT.equals(expectedServiceAvailabilityDate);
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE_SPECIFICATION)
		{
			return serviceSpecification != null;
		}
		else if (featureID == TypesPackage.SERVICE_QUALIFICATION_ITEM__SERVICE)
		{
			return service != null;
		}
		return super.eIsSet(featureID);
	}
	@Override
	public String toString()
	{
		if (eIsProxy()) return super.toString();
		StringBuilder result = new StringBuilder(super.toString());
		result.append(" (id: ");
		result.append(id);
		result.append(", qualificationResult: ");
		result.append(qualificationResult);
		result.append(", expectedServiceAvailabilityDate: ");
		result.append(expectedServiceAvailabilityDate);
		result.append(')');
		return result.toString();
	}
} //ServiceQualificationItemImpl_EXPR