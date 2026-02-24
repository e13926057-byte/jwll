from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models.models import Cart, CartItem, Product
from schemas.schemas import CartItemCreate, CartItemResponse, CartResponse
from routers.auth import get_current_user
from models.models import User

router = APIRouter(prefix="/api/cart", tags=["Cart"])


def get_or_create_cart(user_id: int, db: Session):
    cart = db.query(Cart).filter(Cart.user_id == user_id).first()
    if not cart:
        cart = Cart(user_id=user_id)
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart


@router.get("", response_model=CartResponse)
def get_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(current_user.id, db)
    return cart


@router.post("/items", response_model=CartItemResponse)
def add_to_cart(
    item: CartItemCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(current_user.id, db)
    
    product = db.query(Product).filter(Product.id == item.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    existing_item = db.query(CartItem).filter(
        CartItem.cart_id == cart.id,
        CartItem.product_id == item.product_id
    ).first()
    
    if existing_item:
        existing_item.quantity += item.quantity
        db.commit()
        db.refresh(existing_item)
        return existing_item
    
    new_item = CartItem(
        cart_id=cart.id,
        product_id=item.product_id,
        quantity=item.quantity
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return new_item


@router.delete("/items/{item_id}")
def remove_from_cart(
    item_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(current_user.id, db)
    
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    db.delete(item)
    db.commit()
    return {"message": "Item removed from cart"}


@router.put("/items/{item_id}")
def update_cart_item(
    item_id: int,
    quantity: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(current_user.id, db)
    
    item = db.query(CartItem).filter(
        CartItem.id == item_id,
        CartItem.cart_id == cart.id
    ).first()
    
    if not item:
        raise HTTPException(status_code=404, detail="Item not found in cart")
    
    if quantity <= 0:
        db.delete(item)
        db.commit()
        return {"message": "Item removed from cart"}
    
    item.quantity = quantity
    db.commit()
    db.refresh(item)
    return item


@router.delete("")
def clear_cart(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    cart = get_or_create_cart(current_user.id, db)
    db.query(CartItem).filter(CartItem.cart_id == cart.id).delete()
    db.commit()
    return {"message": "Cart cleared"}
