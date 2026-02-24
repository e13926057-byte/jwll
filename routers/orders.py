from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.models import Order, OrderItem, Cart, CartItem, Product, OrderStatus
from schemas.schemas import OrderCreate, OrderResponse, OrderUpdate, OrderItemResponse
from routers.auth import get_current_user
from models.models import User

router = APIRouter(prefix="/api/orders", tags=["Orders"])


@router.get("", response_model=List[OrderResponse])
def get_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).filter(Order.user_id == current_user.id).all()
    return orders


@router.get("/{order_id}", response_model=OrderResponse)
def get_order(
    order_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(
        Order.id == order_id,
        Order.user_id == current_user.id
    ).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    return order


@router.post("", response_model=OrderResponse)
def create_order(
    order_data: OrderCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = db.query(Cart).filter(Cart.user_id == current_user.id).first()
    if not cart or not cart.items:
        raise HTTPException(status_code=400, detail="Cart is empty")
    
    total_amount = 0
    order_items = []
    
    for item in cart.items:
        product = item.product
        subtotal = product.price * item.quantity
        total_amount += subtotal
        order_items.append(OrderItem(
            product_id=product.id,
            quantity=item.quantity,
            unit_price=product.price,
            subtotal=subtotal
        ))
    
    new_order = Order(
        user_id=current_user.id,
        payment_method_id=order_data.payment_method_id,
        total_amount=total_amount,
        shipping_address=order_data.shipping_address,
        transfer_receipt=order_data.transfer_receipt,
        status=OrderStatus.PENDING
    )
    db.add(new_order)
    db.flush()
    
    for item in order_items:
        item.order_id = new_order.id
        db.add(item)
    
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    db.refresh(new_order)
    return new_order


@router.put("/{order_id}/status", response_model=OrderResponse)
def update_order_status(
    order_id: int,
    order_update: OrderUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order_update.status:
        order.status = OrderStatus[order_update.status.value.upper()]
    if order_update.jeweler_price_offer:
        order.jeweler_price_offer = order_update.jeweler_price_offer
    
    db.commit()
    db.refresh(order)
    return order


@router.get("/admin/all", response_model=List[OrderResponse])
def get_all_orders(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    orders = db.query(Order).all()
    return orders
