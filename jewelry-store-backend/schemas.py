from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
from models import OrderStatus, DesignRequestStatus

class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class JewelerBase(BaseModel):
    name: str
    shop_name: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: EmailStr
    rating: Optional[Decimal] = None

class JewelerCreate(JewelerBase):
    pass

class JewelerResponse(JewelerBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class CategoryBase(BaseModel):
    name: str
    parent_id: Optional[int] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    
    class Config:
        from_attributes = True

class ProductImageBase(BaseModel):
    image_path: str
    display_order: Optional[int] = 0

class ProductImageCreate(ProductImageBase):
    pass

class ProductImageResponse(ProductImageBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ProductBase(BaseModel):
    name: str
    material: Optional[str] = None
    karat: Optional[str] = None
    weight: Optional[Decimal] = None
    price: Decimal
    stock_quantity: int = 0
    description: Optional[str] = None
    image_path: Optional[str] = None

class ProductCreate(ProductBase):
    jeweler_id: int
    category_ids: Optional[List[int]] = []

class ProductResponse(ProductBase):
    id: int
    jeweler_id: int
    created_at: datetime
    jeweler: Optional[JewelerResponse] = None
    images: List[ProductImageResponse] = []
    categories: List[CategoryResponse] = []
    
    class Config:
        from_attributes = True

class ProductFilter(BaseModel):
    category_id: Optional[int] = None
    jeweler_id: Optional[int] = None
    material: Optional[str] = None
    min_price: Optional[Decimal] = None
    max_price: Optional[Decimal] = None

class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1

class CartItemCreate(CartItemBase):
    pass

class CartItemResponse(CartItemBase):
    id: int
    added_at: datetime
    product: Optional[ProductResponse] = None
    
    class Config:
        from_attributes = True

class CartResponse(BaseModel):
    id: int
    user_id: int
    updated_at: datetime
    items: List[CartItemResponse] = []
    
    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: Decimal
    subtotal: Decimal

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    product: Optional[ProductResponse] = None
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    payment_method_id: int
    shipping_address: str
    transfer_receipt: Optional[str] = None

class OrderCreate(BaseModel):
    payment_method_id: int
    shipping_address: str

class OrderUpdate(BaseModel):
    status: Optional[OrderStatus] = None
    transfer_receipt: Optional[str] = None

class OrderResponse(BaseModel):
    id: int
    user_id: int
    payment_method_id: int
    order_date: datetime
    status: OrderStatus
    total_amount: Decimal
    shipping_address: str
    transfer_receipt: Optional[str] = None
    items: List[OrderItemResponse] = []
    
    class Config:
        from_attributes = True

class PaymentMethodBase(BaseModel):
    method_name: str
    qr_code_image: Optional[str] = None
    is_active: bool = True
    notes: Optional[str] = None

class PaymentMethodCreate(PaymentMethodBase):
    pass

class PaymentMethodResponse(PaymentMethodBase):
    id: int
    
    class Config:
        from_attributes = True

class GenerateDesignRequest(BaseModel):
    type: str
    color: str
    shape: str
    material: str
    karat: str
    gemstone_type: str
    gemstone_color: str

class GenerateDesignResponse(BaseModel):
    id: int
    generated_image_url: str
    message: str

class UserGeneratedDesignResponse(BaseModel):
    id: int
    user_id: int
    selected_options: str
    generated_image_url: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class DesignRequestBase(BaseModel):
    jeweler_id: int
    generated_design_id: Optional[int] = None
    description: str
    attachment_url: Optional[str] = None
    estimated_budget: Optional[Decimal] = None

class DesignRequestCreate(DesignRequestBase):
    pass

class DesignRequestUpdate(BaseModel):
    status: Optional[DesignRequestStatus] = None
    jeweler_price_offer: Optional[Decimal] = None

class DesignRequestResponse(DesignRequestBase):
    id: int
    user_id: int
    request_date: datetime
    jeweler_price_offer: Optional[Decimal] = None
    status: DesignRequestStatus
    user: Optional[UserResponse] = None
    jeweler: Optional[JewelerResponse] = None
    generated_design: Optional[UserGeneratedDesignResponse] = None
    
    class Config:
        from_attributes = True