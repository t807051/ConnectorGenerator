package com.telus.connector.svcqualification.api.datatypes.impl;
import com.iisy.solvatio.domain.impl.BaseStructImpl;
import com.telus.connector.svcqualification.api.datatypes.ServiceSpecification;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.impl.ENotificationImpl;
public class ServiceSpecificationImpl_EXPR extends BaseStructImpl implements ServiceSpecification
{
	private static final long serialVersionUID = 1L;
	protected static final String NAME_EDEFAULT = null;
	protected String name = NAME_EDEFAULT;
	public ServiceSpecificationImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.ServiceSpecification";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getServiceSpecification();
	}
	@Override
	public String getName()
	{
		return name;
	}
	@Override
	public void setName(String newName)
	{
		newName = processNewValue(name, newName);
		String oldName = name;
		name = newName;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.SERVICE_SPECIFICATION__NAME, oldName, name));
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.SERVICE_SPECIFICATION__NAME)
		{
			return getName();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.SERVICE_SPECIFICATION__NAME)
		{
			setName((String)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.SERVICE_SPECIFICATION__NAME)
		{
			setName(NAME_EDEFAULT);
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.SERVICE_SPECIFICATION__NAME)
		{
			return NAME_EDEFAULT == null ? name != null : !NAME_EDEFAULT.equals(name);
		}
		return super.eIsSet(featureID);
	}
	@Override
	public String toString()
	{
		if (eIsProxy()) return super.toString();
		StringBuilder result = new StringBuilder(super.toString());
		result.append(" (name: ");
		result.append(name);
		result.append(')');
		return result.toString();
	}
} //ServiceSpecificationImpl_EXPR