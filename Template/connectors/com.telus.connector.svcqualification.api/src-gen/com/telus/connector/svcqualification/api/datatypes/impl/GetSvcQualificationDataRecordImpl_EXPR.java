package com.telus.connector.svcqualification.api.datatypes.impl;
import com.telus.common.api.datatypes.impl.AbstractDataRecordImpl_EXPR;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationDataRecord;
import com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationEntity;
import com.telus.connector.svcqualification.api.datatypes.TypesPackage;
import org.eclipse.emf.common.notify.Notification;
import org.eclipse.emf.common.notify.NotificationChain;
import org.eclipse.emf.ecore.EClass;
import org.eclipse.emf.ecore.InternalEObject;
import org.eclipse.emf.ecore.impl.ENotificationImpl;
public class GetSvcQualificationDataRecordImpl_EXPR extends AbstractDataRecordImpl_EXPR implements GetSvcQualificationDataRecord
{
	private static final long serialVersionUID = 1L;
	protected GetSvcQualificationEntity svcQualificationEntity;
	public GetSvcQualificationDataRecordImpl_EXPR()
	{
		super();
		this.fqn = "com.telus.connector.svcqualification.api.datatypes.GetSvcQualificationDataRecord";
	}
	@Override
	protected EClass eStaticClass()
	{
		return TypesPackage.eINSTANCE.getGetSvcQualificationDataRecord();
	}
	@Override
	public GetSvcQualificationEntity getSvcQualificationEntity()
	{
		if (svcQualificationEntity != null && ((InternalEObject) svcQualificationEntity).eIsProxy())
		{
			InternalEObject oldSvcQualificationEntity = (InternalEObject)svcQualificationEntity;
			svcQualificationEntity = (GetSvcQualificationEntity)eResolveProxy(oldSvcQualificationEntity);
			if (svcQualificationEntity != oldSvcQualificationEntity)
			{
				InternalEObject newSvcQualificationEntity = (InternalEObject)svcQualificationEntity;
				NotificationChain msgs = oldSvcQualificationEntity.eInverseRemove(this, EOPPOSITE_FEATURE_BASE - TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY, null, null);
				if (newSvcQualificationEntity.eInternalContainer() == null)
				{
					msgs = newSvcQualificationEntity.eInverseAdd(this, EOPPOSITE_FEATURE_BASE - TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY, null, msgs);
				}
				if (msgs != null) msgs.dispatch();
				if (eNotificationRequired())
					eNotify(new ENotificationImpl(this, Notification.RESOLVE, TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY, oldSvcQualificationEntity, svcQualificationEntity));
			}
		}
		return svcQualificationEntity;
	}
	public GetSvcQualificationEntity basicGetSvcQualificationEntity()
	{
		return svcQualificationEntity;
	}
	public NotificationChain basicSetSvcQualificationEntity(GetSvcQualificationEntity newSvcQualificationEntity, NotificationChain msgs)
	{
		GetSvcQualificationEntity oldSvcQualificationEntity = svcQualificationEntity;
		svcQualificationEntity = newSvcQualificationEntity;
		if (eNotificationRequired())
		{
			ENotificationImpl notification = new ENotificationImpl(this, Notification.SET, TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY, oldSvcQualificationEntity, newSvcQualificationEntity);
			if (msgs == null) msgs = notification; else msgs.add(notification);
		}
		return msgs;
	}
	@Override
	public void setSvcQualificationEntity(GetSvcQualificationEntity newSvcQualificationEntity)
	{
		newSvcQualificationEntity = processNewValue(svcQualificationEntity, newSvcQualificationEntity);
		if (newSvcQualificationEntity != svcQualificationEntity)
		{
			NotificationChain msgs = null;
			if (svcQualificationEntity != null)
				msgs = ((InternalEObject)svcQualificationEntity).eInverseRemove(this, EOPPOSITE_FEATURE_BASE - TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY, null, msgs);
			if (newSvcQualificationEntity != null)
				msgs = ((InternalEObject)newSvcQualificationEntity).eInverseAdd(this, EOPPOSITE_FEATURE_BASE - TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY, null, msgs);
			msgs = basicSetSvcQualificationEntity(newSvcQualificationEntity, msgs);
			if (msgs != null) msgs.dispatch();
		}
		else if (eNotificationRequired())
			eNotify(new ENotificationImpl(this, Notification.SET, TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY, newSvcQualificationEntity, newSvcQualificationEntity));
	}
	@Override
	public NotificationChain eInverseRemove(InternalEObject otherEnd, int featureID, NotificationChain msgs)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY)
		{
			return basicSetSvcQualificationEntity(null, msgs);
		}
		return super.eInverseRemove(otherEnd, featureID, msgs);
	}
	@Override
	public Object eGet(int featureID, boolean resolve, boolean coreType)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY)
		{
			if (resolve) return getSvcQualificationEntity();
			return basicGetSvcQualificationEntity();
		}
		return super.eGet(featureID, resolve, coreType);
	}
	@Override
	public void eSet(int featureID, Object newValue)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY)
		{
			setSvcQualificationEntity((GetSvcQualificationEntity)newValue);
			return;
		}
		super.eSet(featureID, newValue);
	}
	@Override
	public void eUnset(int featureID)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY)
		{
			setSvcQualificationEntity((GetSvcQualificationEntity)null);
			return;
		}
		super.eUnset(featureID);
	}
	@Override
	public boolean eIsSet(int featureID)
	{
		if (featureID == TypesPackage.GET_SVC_QUALIFICATION_DATA_RECORD__SVC_QUALIFICATION_ENTITY)
		{
			return svcQualificationEntity != null;
		}
		return super.eIsSet(featureID);
	}
} //GetSvcQualificationDataRecordImpl_EXPR