import os
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, Text, ForeignKey, Enum, JSON, Enum
from sqlalchemy.orm import relationship
from database import Base
import enum


class OrderStatus(enum.Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    SHIPPED = "shipped"
    DELIVERED = "delivered"
    CANCELLED = "cancelled"


class DesignRequestStatus(enum.Enum):
    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    COMPLETED = "completed"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, nullable=False, index=True)
    password = Column(String(255), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    phone = Column(String(20))
    dob = Column(DateTime, nullable=True)
    gender = Column(String(10))
    address = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    jeweler = relationship("Jeweler", back_populates="user", uselist=False)
    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
    design_requests = relationship("DesignRequest", back_populates="user")
    generated_designs = relationship("UserGeneratedDesign", back_populates="user")


class Jeweler(Base):
    __tablename__ = "jewelers"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    name = Column(String(100), nullable=False)
    shop_name = Column(String(100))
    bio = Column(Text)
    address = Column(Text)
    phone = Column(String(20))
    email = Column(String(100))
    rating = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="jeweler")
    products = relationship("Product", back_populates="jeweler")
    design_requests = relationship("DesignRequest", back_populates="jeweler")


class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    method_name = Column(String(50), nullable=False)
    qr_code_image = Column(String(255))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)

    orders = relationship("Order", back_populates="payment_method")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    parent_id = Column(Integer, ForeignKey("categories.id"), nullable=True)

    parent = relationship("Category", remote_side=[id], backref="subcategories")
    products = relationship("Product", secondary="product_categories", back_populates="categories")


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    jeweler_id = Column(Integer, ForeignKey("jewelers.id"))
    name = Column(String(100), nullable=False)
    material = Column(String(50))
    karat = Column(String(10))
    weight = Column(Float)
    price = Column(Float, nullable=False)
    stock_quantity = Column(Integer, default=0)
    description = Column(Text)
    image_path = Column(String(255))

    jeweler = relationship("Jeweler", back_populates="products")
    images = relationship("ProductImage", back_populates="product")
    categories = relationship("Category", secondary="product_categories", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")


class ProductImage(Base):
    __tablename__ = "product_images"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    image_path = Column(String(255))
    display_order = Column(Integer, default=0)

    product = relationship("Product", back_populates="images")


class ProductCategory(Base):
    __tablename__ = "product_categories"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    category_id = Column(Integer, ForeignKey("categories.id"))


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart")


class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)

    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    payment_method_id = Column(Integer, ForeignKey("payment_methods.id"))
    order_date = Column(DateTime, default=datetime.utcnow)
    status = Column(Enum(OrderStatus), default=OrderStatus.PENDING)
    total_amount = Column(Float, nullable=False)
    shipping_address = Column(Text)
    transfer_receipt = Column(String(255))

    user = relationship("User", back_populates="orders")
    payment_method = relationship("PaymentMethod", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")


class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    quantity = Column(Integer, default=1)
    unit_price = Column(Float, nullable=False)
    subtotal = Column(Float, nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")


class UserGeneratedDesign(Base):
    __tablename__ = "user_generated_designs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    selected_options = Column(JSON)
    generated_image_url = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="generated_designs")


class DesignRequest(Base):
    __tablename__ = "design_requests"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    jeweler_id = Column(Integer, ForeignKey("jewelers.id"))
    generated_design_id = Column(Integer, ForeignKey("user_generated_designs.id"), nullable=True)
    request_date = Column(DateTime, default=datetime.utcnow)
    description = Column(Text)
    attachment_url = Column(String(255))
    estimated_budget = Column(Float)
    jeweler_price_offer = Column(Float, nullable=True)
    status = Column(Enum(DesignRequestStatus), default=DesignRequestStatus.PENDING)

    user = relationship("User", back_populates="design_requests")
    jeweler = relationship("Jeweler", back_populates="design_requests")
    generated_design = relationship("UserGeneratedDesign")
