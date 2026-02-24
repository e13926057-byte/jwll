from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.models import PaymentMethod
from schemas.schemas import PaymentMethodCreate, PaymentMethodResponse
from routers.auth import get_current_user
from models.models import User

router = APIRouter(prefix="/api/payment-methods", tags=["Payment Methods"])


@router.get("", response_model=List[PaymentMethodResponse])
def get_payment_methods(db: Session = Depends(get_db)):
    methods = db.query(PaymentMethod).filter(PaymentMethod.is_active == True).all()
    return methods


@router.post("", response_model=PaymentMethodResponse)
def create_payment_method(
    payment_method: PaymentMethodCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    new_method = PaymentMethod(
        method_name=payment_method.method_name,
        qr_code_image=payment_method.qr_code_image,
        is_active=payment_method.is_active,
        notes=payment_method.notes
    )
    db.add(new_method)
    db.commit()
    db.refresh(new_method)
    return new_method


@router.put("/{method_id}", response_model=PaymentMethodResponse)
def update_payment_method(
    method_id: int,
    payment_method: PaymentMethodCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    db_method = db.query(PaymentMethod).filter(PaymentMethod.id == method_id).first()
    if not db_method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    
    db_method.method_name = payment_method.method_name
    db_method.qr_code_image = payment_method.qr_code_image
    db_method.is_active = payment_method.is_active
    db_method.notes = payment_method.notes
    
    db.commit()
    db.refresh(db_method)
    return db_method


@router.delete("/{method_id}")
def delete_payment_method(
    method_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    method = db.query(PaymentMethod).filter(PaymentMethod.id == method_id).first()
    if not method:
        raise HTTPException(status_code=404, detail="Payment method not found")
    
    method.is_active = False
    db.commit()
    return {"message": "Payment method deactivated"}
