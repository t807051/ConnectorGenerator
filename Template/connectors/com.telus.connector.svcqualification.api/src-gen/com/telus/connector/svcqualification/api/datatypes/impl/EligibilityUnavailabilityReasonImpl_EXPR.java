package com.telus.connector.svcqualification.api.datatypes.impl;
import com.iisy.solvatio.domain.impl.BaseStructImpl;
import com.telus.connector.svcqualification.api.datatypes.EligibilityUnavailabilityReason;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.impl.ENotificationImpl;
public class EligibilityUnavailabilityReasonImpl_EXPR extends BaseStructImpl implements EligibilityUnavailabilityReason
{
	private static final long serialVersionUID = 1L;
	protected static final String LABEL_EDEFAULT = null;
	protected String label = LABEL_EDEFAULT;
	protected static final Integer CODE_EDEFAULT = null;
	protected Integer code = CODE_EDEFAULT;
	public EligibilityUnavailabilityReasonImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.EligibilityUnavailabilityReason";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getEligibilityUnavailabilityReason();
	}
	@Override
	public String getLabel()
	{
		return label;
	}
	@Override
	public void setLabel(String newLabel)
	{
		newLabel = processNewValue(label, newLabel);
		String oldLabel = label;
		label = newLabel;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__LABEL, oldLabel, label));
	}
	@Override
	public Integer getCode()
	{
		return code;
	}
	@Override
	public void setCode(Integer newCode)
	{
		newCode = processNewValue(code, newCode);
		Integer oldCode = code;
		code = newCode;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__CODE, oldCode, code));
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__LABEL)
		{
			return getLabel();
		}
		else if (featureID == TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__CODE)
		{
			return getCode();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__LABEL)
		{
			setLabel((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__CODE)
		{
			setCode((Integer)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__LABEL)
		{
			setLabel(LABEL_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__CODE)
		{
			setCode(CODE_EDEFAULT);
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__LABEL)
		{
			return LABEL_EDEFAULT == null ? label != null : !LABEL_EDEFAULT.equals(label);
		}
		else if (featureID == TypesPackage.ELIGIBILITY_UNAVAILABILITY_REASON__CODE)
		{
			return CODE_EDEFAULT == null ? code != null : !CODE_EDEFAULT.equals(code);
		}
		return super.eIsSet(featureID);
	}
	@Override
	public String toString()
	{
		if (eIsProxy()) return super.toString();
		StringBuilder result = new StringBuilder(super.toString());
		result.append(" (label: ");
		result.append(label);
		result.append(", code: ");
		result.append(code);
		result.append(')');
		return result.toString();
	}
} //EligibilityUnavailabilityReasonImpl_EXPR