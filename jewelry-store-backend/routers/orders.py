from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from services.auth import get_current_active_user
import models
import schemas
from decimal import Decimal

router = APIRouter(prefix="/api/orders", tags=["Orders"])

@router.get("/", response_model=List[schemas.OrderResponse])
def get_orders(
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    orders = db.query(models.Order).filter(
        models.Order.user_id == current_user.id
    ).order_by(models.Order.order_date.desc()).all()
    return orders

@router.get("/{order_id}", response_model=schemas.OrderResponse)
def get_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

@router.post("/", response_model=schemas.OrderResponse)
def create_order(
    order_data: schemas.OrderCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    cart = db.query(models.Cart).filter(
        models.Cart.user_id == current_user.id
    ).first()
    
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total_amount = Decimal('0')
    order_items_data = []
    
    for cart_item in cart.items:
        product = cart_item.product
        if product.stock_quantity < cart_item.quantity:
            raise HTTPException(
                status_code=400,
                detail=f"Insufficient stock for {product.name}"
            )
        
        subtotal = product.price * cart_item.quantity
        total_amount += subtotal
        
        order_items_data.append({
            'product_id': product.id,
            'quantity': cart_item.quantity,
            'unit_price': product.price,
            'subtotal': subtotal
        })
        
        product.stock_quantity -= cart_item.quantity
    
    order = models.Order(
        user_id=current_user.id,
        payment_method_id=order_data.payment_method_id,
        total_amount=total_amount,
        shipping_address=order_data.shipping_address,
        status=models.OrderStatus.pending
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    
    for item_data in order_items_data:
        order_item = models.OrderItem(
            order_id=order.id,
            **item_data
        )
        db.add(order_item)
    
    db.query(models.CartItem).filter(models.CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(order)
    
    return order

@router.put("/{order_id}", response_model=schemas.OrderResponse)
def update_order(
    order_id: int,
    order_update: schemas.OrderUpdate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    order = db.query(models.Order).filter(
        models.Order.id == order_id,
        models.Order.user_id == current_user.id
    ).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order_update.status:
        order.status = order_update.status
    if order_update.transfer_receipt:
        order.transfer_receipt = order_update.transfer_receipt
    
    db.commit()
    db.refresh(order)
    return order