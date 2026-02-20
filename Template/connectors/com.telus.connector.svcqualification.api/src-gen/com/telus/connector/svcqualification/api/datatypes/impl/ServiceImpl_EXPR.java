package com.telus.connector.svcqualification.api.datatypes.impl;
import com.iisy.solvatio.domain.impl.BaseStructImpl;
import com.telus.connector.svcqualification.api.datatypes.Characteristic;
import com.telus.connector.svcqualification.api.datatypes.EligibilityUnavailabilityReason;
import com.telus.connector.svcqualification.api.datatypes.Place;
import com.telus.connector.svcqualification.api.datatypes.Service;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import java.util.Collection;
import java.util.List;
import org.eclipse.emf.common.notify.NotificationChain;
import org.eclipse.emf.common.util.EList;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.InternalEObject;
import org.eclipse.emf.ecore.util.EObjectContainmentEList;
import org.eclipse.emf.ecore.util.InternalEList;
public class ServiceImpl_EXPR extends BaseStructImpl implements Service
{
	private static final long serialVersionUID = 1L;
	protected EList<Characteristic> characteristic;
	protected EList<Place> place;
	protected EList<EligibilityUnavailabilityReason> eligibilityUnavailabilityReason;
	public ServiceImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.Service";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getService();
	}
	@Override
	public List<Characteristic> getCharacteristic()
	{
		if (characteristic == null)
		{
			characteristic = createContainmentEListResolving(Characteristic.class, this, TypesPackage.SERVICE__CHARACTERISTIC);
		}
		return characteristic;
	}
	@Override
	public List<Place> getPlace()
	{
		if (place == null)
		{
			place = createContainmentEListResolving(Place.class, this, TypesPackage.SERVICE__PLACE);
		}
		return place;
	}
	@Override
	public List<EligibilityUnavailabilityReason> getEligibilityUnavailabilityReason()
	{
		if (eligibilityUnavailabilityReason == null)
		{
			eligibilityUnavailabilityReason = createContainmentEListResolving(EligibilityUnavailabilityReason.class, this, TypesPackage.SERVICE__ELIGIBILITY_UNAVAILABILITY_REASON);
		}
		return eligibilityUnavailabilityReason;
	}
	@Override
	public void setCharacteristic(final Collection<? extends Characteristic> value)
	{
		getCharacteristic().clear(); getCharacteristic().addAll(value);
	}
	@Override
	public void setPlace(final Collection<? extends Place> value)
	{
		getPlace().clear(); getPlace().addAll(value);
	}
	@Override
	public void setEligibilityUnavailabilityReason(final Collection<? extends EligibilityUnavailabilityReason> value)
	{
		getEligibilityUnavailabilityReason().clear(); getEligibilityUnavailabilityReason().addAll(value);
	}
	@Override
	public NotificationChain eInverseRemove(InternalEObject otherEnd, int featureID, NotificationChain msgs)
	{
		if (featureID == TypesPackage.SERVICE__CHARACTERISTIC)
		{
			return ((InternalEList<?>)getCharacteristic()).basicRemove(otherEnd, msgs);
		}
		else if (featureID == TypesPackage.SERVICE__PLACE)
		{
			return ((InternalEList<?>)getPlace()).basicRemove(otherEnd, msgs);
		}
		else if (featureID == TypesPackage.SERVICE__ELIGIBILITY_UNAVAILABILITY_REASON)
		{
			return ((InternalEList<?>)getEligibilityUnavailabilityReason()).basicRemove(otherEnd, msgs);
		}
		return super.eInverseRemove(otherEnd, featureID, msgs);
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.SERVICE__CHARACTERISTIC)
		{
			return getCharacteristic();
		}
		else if (featureID == TypesPackage.SERVICE__PLACE)
		{
			return getPlace();
		}
		else if (featureID == TypesPackage.SERVICE__ELIGIBILITY_UNAVAILABILITY_REASON)
		{
			return getEligibilityUnavailabilityReason();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@SuppressWarnings("unchecked")
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.SERVICE__CHARACTERISTIC)
		{
			getCharacteristic().clear();
			getCharacteristic().addAll((Collection<? extends Characteristic>)newValue);
			return;
		}
		else if (featureID == TypesPackage.SERVICE__PLACE)
		{
			getPlace().clear();
			getPlace().addAll((Collection<? extends Place>)newValue);
			return;
		}
		else if (featureID == TypesPackage.SERVICE__ELIGIBILITY_UNAVAILABILITY_REASON)
		{
			getEligibilityUnavailabilityReason().clear();
			getEligibilityUnavailabilityReason().addAll((Collection<? extends EligibilityUnavailabilityReason>)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.SERVICE__CHARACTERISTIC)
		{
			getCharacteristic().clear();
			return;
		}
		else if (featureID == TypesPackage.SERVICE__PLACE)
		{
			getPlace().clear();
			return;
		}
		else if (featureID == TypesPackage.SERVICE__ELIGIBILITY_UNAVAILABILITY_REASON)
		{
			getEligibilityUnavailabilityReason().clear();
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.SERVICE__CHARACTERISTIC)
		{
			return characteristic != null && !characteristic.isEmpty();
		}
		else if (featureID == TypesPackage.SERVICE__PLACE)
		{
			return place != null && !place.isEmpty();
		}
		else if (featureID == TypesPackage.SERVICE__ELIGIBILITY_UNAVAILABILITY_REASON)
		{
			return eligibilityUnavailabilityReason != null && !eligibilityUnavailabilityReason.isEmpty();
		}
		return super.eIsSet(featureID);
	}
} //ServiceImpl_EXPR