from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
from enum import Enum


class OrderStatusEnum(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class DesignRequestStatusEnum(str, Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"


class UserBase(BaseModel):
    username: str
    email: EmailStr
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    dob: Optional[datetime] = None
    gender: Optional[str] = None
    address: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class JewelerBase(BaseModel):
    name: str
    shop_name: Optional[str] = None
    bio: Optional[str] = None
    address: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    rating: Optional[float] = 0.0


class JewelerCreate(JewelerBase):
    user_id: int


class JewelerResponse(JewelerBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class PaymentMethodBase(BaseModel):
    method_name: str
    qr_code_image: Optional[str] = None
    is_active: Optional[bool] = True
    notes: Optional[str] = None


class PaymentMethodCreate(PaymentMethodBase):
    pass


class PaymentMethodResponse(PaymentMethodBase):
    id: int

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

    class Config:
        from_attributes = True


class ProductBase(BaseModel):
    name: str
    material: Optional[str] = None
    karat: Optional[str] = None
    weight: Optional[float] = None
    price: float
    stock_quantity: Optional[int] = 0
    description: Optional[str] = None
    image_path: Optional[str] = None
    category_ids: Optional[List[int]] = []


class ProductCreate(ProductBase):
    jeweler_id: int


class ProductUpdate(BaseModel):
    name: Optional[str] = None
    material: Optional[str] = None
    karat: Optional[str] = None
    weight: Optional[float] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    description: Optional[str] = None
    image_path: Optional[str] = None
    category_ids: Optional[List[int]] = None


class ProductResponse(ProductBase):
    id: int
    jeweler_id: int
    images: List[ProductImageResponse] = []

    class Config:
        from_attributes = True


class CartItemBase(BaseModel):
    product_id: int
    quantity: int = 1


class CartItemCreate(CartItemBase):
    pass


class CartItemResponse(CartItemBase):
    id: int
    product: ProductResponse

    class Config:
        from_attributes = True


class CartBase(BaseModel):
    user_id: int


class CartResponse(CartBase):
    id: int
    updated_at: datetime
    items: List[CartItemResponse] = []

    class Config:
        from_attributes = True


class OrderItemBase(BaseModel):
    product_id: int
    quantity: int = 1
    unit_price: float
    subtotal: float


class OrderItemResponse(OrderItemBase):
    id: int

    class Config:
        from_attributes = True


class OrderBase(BaseModel):
    payment_method_id: int
    total_amount: float
    shipping_address: Optional[str] = None
    transfer_receipt: Optional[str] = None


class OrderCreate(OrderBase):
    pass


class OrderUpdate(BaseModel):
    status: Optional[OrderStatusEnum] = None
    jeweler_price_offer: Optional[float] = None


class OrderResponse(OrderBase):
    id: int
    user_id: int
    order_date: datetime
    status: OrderStatusEnum
    items: List[OrderItemResponse] = []

    class Config:
        from_attributes = True


class UserGeneratedDesignBase(BaseModel):
    selected_options: str
    generated_image_url: str


class UserGeneratedDesignCreate(UserGeneratedDesignBase):
    user_id: int


class UserGeneratedDesignResponse(UserGeneratedDesignBase):
    id: int
    user_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class DesignRequestBase(BaseModel):
    jeweler_id: int
    description: Optional[str] = None
    attachment_url: Optional[str] = None
    estimated_budget: Optional[float] = None
    generated_design_id: Optional[int] = None


class DesignRequestCreate(DesignRequestBase):
    pass


class DesignRequestUpdate(BaseModel):
    jeweler_price_offer: Optional[float] = None
    status: Optional[DesignRequestStatusEnum] = None


class DesignRequestResponse(DesignRequestBase):
    id: int
    user_id: int
    request_date: datetime
    jeweler_price_offer: Optional[float] = None
    status: DesignRequestStatusEnum

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class LoginRequest(BaseModel):
    username: str
    password: str


class AIGenerateDesignRequest(BaseModel):
    type: str
    color: str
    shape: str
    material: str
    karat: str
    gemstone_type: str
    gemstone_color: str
