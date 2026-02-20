package com.telus.connector.svcqualification.api.datatypes.impl;
import com.iisy.solvatio.domain.impl.BaseStructImpl;
import com.telus.connector.svcqualification.api.datatypes.Place;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.impl.ENotificationImpl;
public class PlaceImpl_EXPR extends BaseStructImpl implements Place
{
	private static final long serialVersionUID = 1L;
	protected static final String ROLE_EDEFAULT = null;
	protected String role = ROLE_EDEFAULT;
	protected static final String ID_EDEFAULT = null;
	protected String id = ID_EDEFAULT;
	public PlaceImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.Place";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getPlace();
	}
	@Override
	public String getRole()
	{
		return role;
	}
	@Override
	public void setRole(String newRole)
	{
		newRole = processNewValue(role, newRole);
		String oldRole = role;
		role = newRole;
		if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.PLACE__ROLE, oldRole, role));
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
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.PLACE__ID, oldId, id));
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.PLACE__ROLE)
		{
			return getRole();
		}
		else if (featureID == TypesPackage.PLACE__ID)
		{
			return getId();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.PLACE__ROLE)
		{
			setRole((String)newValue);
			return;
		}
		else if (featureID == TypesPackage.PLACE__ID)
		{
			setId((String)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.PLACE__ROLE)
		{
			setRole(ROLE_EDEFAULT);
			return;
		}
		else if (featureID == TypesPackage.PLACE__ID)
		{
			setId(ID_EDEFAULT);
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.PLACE__ROLE)
		{
			return ROLE_EDEFAULT == null ? role != null : !ROLE_EDEFAULT.equals(role);
		}
		else if (featureID == TypesPackage.PLACE__ID)
		{
			return ID_EDEFAULT == null ? id != null : !ID_EDEFAULT.equals(id);
		}
		return super.eIsSet(featureID);
	}
	@Override
	public String toString()
	{
		if (eIsProxy()) return super.toString();
		StringBuilder result = new StringBuilder(super.toString());
		result.append(" (role: ");
		result.append(role);
		result.append(", id: ");
		result.append(id);
		result.append(')');
		return result.toString();
	}
} //PlaceImpl_EXPR