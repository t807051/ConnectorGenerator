package com.telus.connector.svcqualification.api.datatypes.impl;
import com.iisy.solvatio.domain.impl.BaseStructImpl;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.impl.ENotificationImpl;
public class GetSvcQualificationRequestImpl_EXPR extends BaseStructImpl implements GetSvcQualificationRequest
{
	private static final long serialVersionUID = 1L;
	protected static final String LPDS_ID_EDEFAULT = null;
	protected String lpdsId = LPDS_ID_EDEFAULT;
	public GetSvcQualificationRequestImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationRequest";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getGetSvcQualificationRequest();
	}
	@Override
	public String getLpdsId()
	{
		return lpdsId;
	}
	@Override
	public void setLpdsId(String newLpdsId)
	{
		newLpdsId = processNewValue(lpdsId, newLpdsId);
		String oldLpdsId = lpdsId;
		lpdsId = newLpdsId;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.GET_SVC_QUALIFICATION_REQUEST__LPDS_ID, oldLpdsId, lpdsId));
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_REQUEST__LPDS_ID)
		{
			return getLpdsId();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_REQUEST__LPDS_ID)
		{
			setLpdsId((String)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_REQUEST__LPDS_ID)
		{
			setLpdsId(LPDS_ID_EDEFAULT);
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_REQUEST__LPDS_ID)
		{
			return LPDS_ID_EDEFAULT == null ? lpdsId != null : !LPDS_ID_EDEFAULT.equals(lpdsId);
		}
		return super.eIsSet(featureID);
	}
	@Override
	public String toString()
	{
		if (eIsProxy()) return super.toString();
		StringBuilder result = new StringBuilder(super.toString());
		result.append(" (lpdsId: ");
		result.append(lpdsId);
		result.append(')');
		return result.toString();
	}
} //GetSvcQualificationRequestImpl_EXPR