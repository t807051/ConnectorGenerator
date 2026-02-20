package com.telus.connector.svcqualification.api.datatypes.impl;
import com.iisy.solvatio.domain.impl.BaseStructImpl;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationEntity;
import com.telus.connector.svcqualification.api.datatypes.ServiceQualificationItem;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import java.util.Collection;
import java.util.List;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.emf.common.notify.NotificationChain;
import org.eclipse.emf.common.util.EList;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.InternalEObject;
import org.eclipse.emf.ecore.impl.ENotificationImpl;
import org.eclipse.emf.ecore.util.EObjectContainmentEList;
import org.eclipse.emf.ecore.util.InternalEList;
public class GetSvcQualificationEntityImpl_EXPR extends BaseStructImpl implements GetSvcQualificationEntity
{
	private static final long serialVersionUID = 1L;
	protected static final String ID_EDEFAULT = null;
	protected String id = ID_EDEFAULT;
	protected static final String QUALIFICATION_RESULT_EDEFAULT = null;
	protected String qualificationResult = QUALIFICATION_RESULT_EDEFAULT;
	protected static final String EXTERNAL_ID_EDEFAULT = null;
	protected String externalId = EXTERNAL_ID_EDEFAULT;
	protected static final String DESCRIPTION_EDEFAULT = null;
	protected String description = DESCRIPTION_EDEFAULT;
	protected EList<ServiceQualificationItem> serviceQualificationItem;
	public GetSvcQualificationEntityImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationEntity";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getGetSvcQualificationEntity();
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
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.GET_SVC_QUALIFICATION_ENTITY__ID, oldId, id));
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
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.GET_SVC_QUALIFICATION_ENTITY__QUALIFICATION_RESULT, oldQualificationResult, qualificationResult));
	}
	@Override
	public String getExternalId()
	{
		return externalId;
	}
	@Override
	public void setExternalId(String newExternalId)
	{
		newExternalId = processNewValue(externalId, newExternalId);
		String oldExternalId = externalId;
		externalId = newExternalId;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.GET_SVC_QUALIFICATION_ENTITY__EXTERNAL_ID, oldExternalId, externalId));
	}
	@Override
	public String getDescription()
	{
		return description;
	}
	@Override
	public void setDescription(String newDescription)
	{
		newDescription = processNewValue(description, newDescription);
		String oldDescription = description;
		description = newDescription;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.GET_SVC_QUALIFICATION_ENTITY__DESCRIPTION, oldDescription, description));
	}
	@Override
	public List<ServiceQualificationItem> getServiceQualificationItem()
	{
		if (serviceQualificationItem == null)
		{
			serviceQualificationItem = createContainmentEListResolving(ServiceQualificationItem.class, this, TypesPackage.GET_SVC_QUALIFICATION_ENTITY__SERVICE_QUALIFICATION_ITEM);
		}
		return serviceQualificationItem;
	}
	@Override
	public void setServiceQualificationItem(final Collection<? extends ServiceQualificationItem> value)
	{
		getServiceQualificationItem().clear(); getServiceQualificationItem().addAll(value);
	}
	@Override
	public NotificationChain eInverseRemove(InternalEObject otherEnd, int featureID, NotificationChain msgs)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__SERVICE_QUALIFICATION_ITEM)
		{
			return ((InternalEList<?>)getServiceQualificationItem()).basicRemove(otherEnd, msgs);
		}
		return super.eInverseRemove(otherEnd, featureID, msgs);
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__ID)
		{
			return getId();
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__QUALIFICATION_RESULT)
		{
			return getQualificationResult();
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__EXTERNAL_ID)
		{
			return getExternalId();
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__DESCRIPTION)
		{
			return getDescription();
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__SERVICE_QUALIFICATION_ITEM)
		{
			return getServiceQualificationItem();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@SuppressWarnings("unchecked")
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__ID)
		{
			setId((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__QUALIFICATION_RESULT)
		{
			setQualificationResult((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__EXTERNAL_ID)
		{
			setExternalId((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__DESCRIPTION)
		{
			setDescription((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__SERVICE_QUALIFICATION_ITEM)
		{
			getServiceQualificationItem().clear();
			getServiceQualificationItem().addAll((Collection<? extends ServiceQualificationItem>)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__ID)
		{
			setId(ID_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__QUALIFICATION_RESULT)
		{
			setQualificationResult(QUALIFICATION_RESULT_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__EXTERNAL_ID)
		{
			setExternalId(EXTERNAL_ID_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__DESCRIPTION)
		{
			setDescription(DESCRIPTION_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__SERVICE_QUALIFICATION_ITEM)
		{
			getServiceQualificationItem().clear();
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__ID)
		{
			return ID_EDEFAULT == null ? id != null : !ID_EDEFAULT.equals(id);
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__QUALIFICATION_RESULT)
		{
			return QUALIFICATION_RESULT_EDEFAULT == null ? qualificationResult != null : !QUALIFICATION_RESULT_EDEFAULT.equals(qualificationResult);
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__EXTERNAL_ID)
		{
			return EXTERNAL_ID_EDEFAULT == null ? externalId != null : !EXTERNAL_ID_EDEFAULT.equals(externalId);
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__DESCRIPTION)
		{
			return DESCRIPTION_EDEFAULT == null ? description != null : !DESCRIPTION_EDEFAULT.equals(description);
		}
		else if (featureID == TypesPackage.GET_SVC_QUALIFICATION_ENTITY__SERVICE_QUALIFICATION_ITEM)
		{
			return serviceQualificationItem != null && !serviceQualificationItem.isEmpty();
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
		result.append(", externalId: ");
		result.append(externalId);
		result.append(", description: ");
		result.append(description);
		result.append(')');
		return result.toString();
	}
} //GetSvcQualificationEntityImpl_EXPR