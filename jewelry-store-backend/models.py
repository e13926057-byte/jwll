from sqlalchemy import Column, Integer, String, Text, Decimal, DateTime, ForeignKey, Enum, Boolean, Date, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import enum

class OrderStatus(enum.Enum):
    pending = "pending"
    paid = "paid"
    processing = "processing"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class DesignRequestStatus(enum.Enum):
    pending = "pending"
    priced = "priced"
    accepted = "accepted"
    in_progress = "in_progress"
    completed = "completed"
    rejected = "rejected"

class User(Base):
    __tablename__ = "Users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String(255), unique=True, index=True)
    password = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    phone = Column(String(255))
    dob = Column(Date)
    gender = Column(String(255))
    address = Column(Text)
    created_at = Column(DateTime, server_default=func.now())
    
    carts = relationship("Cart", back_populates="user")
    orders = relationship("Order", back_populates="user")
    designs = relationship("UserGeneratedDesign", back_populates="user")
    design_requests = relationship("DesignRequest", back_populates="user")

class Jeweler(Base):
    __tablename__ = "Jewelers"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    shop_name = Column(String(255))
    bio = Column(Text)
    address = Column(String(255))
    phone = Column(String(255))
    email = Column(String(255), unique=True, index=True)
    rating = Column(Decimal(3, 2))
    created_at = Column(DateTime, server_default=func.now())
    
    products = relationship("Product", back_populates="jeweler")
    design_requests = relationship("DesignRequest", back_populates="jeweler")

class PaymentMethod(Base):
    __tablename__ = "Payment_Methods"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    method_name = Column(String(255))
    qr_code_image = Column(String(255))
    is_active = Column(Boolean, default=True)
    notes = Column(Text)
    
    orders = relationship("Order", back_populates="payment_method")

class Category(Base):
    __tablename__ = "Categories"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255))
    parent_id = Column(Integer, ForeignKey("Categories.id"), nullable=True)
    
    parent = relationship("Category", remote_side=[id], backref="children")

product_categories = Table(
    "Product_Categories",
    Base.metadata,
    Column("product_id", Integer, ForeignKey("Products.id"), primary_key=True),
    Column("category_id", Integer, ForeignKey("Categories.id"), primary_key=True)
)

class Product(Base):
    __tablename__ = "Products"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    jeweler_id = Column(Integer, ForeignKey("Jewelers.id"))
    name = Column(String(255))
    material = Column(String(255))
    karat = Column(String(255))
    weight = Column(Decimal(10, 2))
    price = Column(Decimal(10, 2))
    stock_quantity = Column(Integer)
    description = Column(Text)
    image_path = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    
    jeweler = relationship("Jeweler", back_populates="products")
    images = relationship("ProductImage", back_populates="product")
    categories = relationship("Category", secondary=product_categories)
    cart_items = relationship("CartItem", back_populates="product")
    order_items = relationship("OrderItem", back_populates="product")

class ProductImage(Base):
    __tablename__ = "Product_Images"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey("Products.id"))
    image_path = Column(String(255))
    display_order = Column(Integer)
    created_at = Column(DateTime, server_default=func.now())
    
    product = relationship("Product", back_populates="images")

class Cart(Base):
    __tablename__ = "Carts"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"), unique=True)
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now())
    
    user = relationship("User", back_populates="carts")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")

class CartItem(Base):
    __tablename__ = "Cart_Items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey("Carts.id"))
    product_id = Column(Integer, ForeignKey("Products.id"))
    quantity = Column(Integer, default=1)
    added_at = Column(DateTime, server_default=func.now())
    
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product", back_populates="cart_items")

class Order(Base):
    __tablename__ = "Orders"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    payment_method_id = Column(Integer, ForeignKey("Payment_Methods.id"))
    order_date = Column(DateTime, server_default=func.now())
    status = Column(Enum(OrderStatus), default=OrderStatus.pending)
    total_amount = Column(Decimal(10, 2))
    shipping_address = Column(Text)
    transfer_receipt = Column(String(255))
    
    user = relationship("User", back_populates="orders")
    payment_method = relationship("PaymentMethod", back_populates="orders")
    items = relationship("OrderItem", back_populates="order")

class OrderItem(Base):
    __tablename__ = "Order_Items"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey("Orders.id"))
    product_id = Column(Integer, ForeignKey("Products.id"))
    quantity = Column(Integer)
    unit_price = Column(Decimal(10, 2))
    subtotal = Column(Decimal(10, 2))
    
    order = relationship("Order", back_populates="items")
    product = relationship("Product", back_populates="order_items")

class UserGeneratedDesign(Base):
    __tablename__ = "User_Generated_Designs"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    selected_options = Column(Text)
    generated_image_url = Column(String(255))
    created_at = Column(DateTime, server_default=func.now())
    
    user = relationship("User", back_populates="designs")
    design_requests = relationship("DesignRequest", back_populates="generated_design")

class DesignRequest(Base):
    __tablename__ = "Design_Requests"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("Users.id"))
    jeweler_id = Column(Integer, ForeignKey("Jewelers.id"))
    generated_design_id = Column(Integer, ForeignKey("User_Generated_Designs.id"), nullable=True)
    request_date = Column(DateTime, server_default=func.now())
    description = Column(Text)
    attachment_url = Column(String(255))
    estimated_budget = Column(Decimal(10, 2))
    jeweler_price_offer = Column(Decimal(10, 2))
    status = Column(Enum(DesignRequestStatus), default=DesignRequestStatus.pending)
    
    user = relationship("User", back_populates="design_requests")
    jeweler = relationship("Jeweler", back_populates="design_requests")
    generated_design = relationship("UserGeneratedDesign", back_populates="design_requests")