package com.telus.connector.svcqualification.api.datatypes.impl;
import com.iisy.solvatio.domain.impl.BaseStructImpl;
import com.telus.connector.svcqualification.api.datatypes.Characteristic;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.impl.ENotificationImpl;
public class CharacteristicImpl_EXPR extends BaseStructImpl implements Characteristic
{
	private static final long serialVersionUID = 1L;
	protected static final String NAME_EDEFAULT = null;
	protected String name = NAME_EDEFAULT;
	protected static final String VALUE_EDEFAULT = null;
	protected String value = VALUE_EDEFAULT;
	public CharacteristicImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.Characteristic";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getCharacteristic();
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
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.CHARACTERISTIC__NAME, oldName, name));
	}
	@Override
	public String getValue()
	{
		return value;
	}
	@Override
	public void setValue(String newValue)
	{
		newValue = processNewValue(value, newValue);
		String oldValue = value;
		value = newValue;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.CHARACTERISTIC__VALUE, oldValue, value));
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.CHARACTERISTIC__NAME)
		{
			return getName();
		}
		else if (featureID == TypesPackage.CHARACTERISTIC__VALUE)
		{
			return getValue();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.CHARACTERISTIC__NAME)
		{
			setName((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.CHARACTERISTIC__VALUE)
		{
			setValue((String)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.CHARACTERISTIC__NAME)
		{
			setName(NAME_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.CHARACTERISTIC__VALUE)
		{
			setValue(VALUE_EDEFAULT);
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.CHARACTERISTIC__NAME)
		{
			return NAME_EDEFAULT == null ? name != null : !NAME_EDEFAULT.equals(name);
		}
		else if (featureID == TypesPackage.CHARACTERISTIC__VALUE)
		{
			return VALUE_EDEFAULT == null ? value != null : !VALUE_EDEFAULT.equals(value);
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
		result.append(", value: ");
		result.append(value);
		result.append(')');
		return result.toString();
	}
} //CharacteristicImpl_EXPR