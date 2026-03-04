from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Jeweler, Category, Product, PaymentMethod
from services.auth import get_password_hash
from decimal import Decimal
import random

DATABASE_URL = "mysql+pymysql://root:@localhost:3306/jewelry_store"

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def seed_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Seeding Users...")
        users = [
            User(username="user1", email="user1@example.com", password=get_password_hash("password123"),
                 first_name="Ahmed", last_name="Ali", phone="0501234567", gender="male"),
            User(username="user2", email="user2@example.com", password=get_password_hash("password123"),
                 first_name="Sara", last_name="Mohammed", phone="0501234568", gender="female"),
            User(username="user3", email="user3@example.com", password=get_password_hash("password123"),
                 first_name="Khalid", last_name="Omar", phone="0501234569", gender="male"),
            User(username="user4", email="user4@example.com", password=get_password_hash("password123"),
                 first_name="Fatima", last_name="Hassan", phone="0501234570", gender="female"),
            User(username="user5", email="user5@example.com", password=get_password_hash("password123"),
                 first_name="Omar", last_name="Khalid", phone="0501234571", gender="male"),
        ]
        for user in users:
            db.add(user)
        db.commit()
        
        print("Seeding Jewelers...")
        jewelers = [
            Jeweler(name="Abdullah Al-Sayed", shop_name="Al-Sayed Jewelry", 
                    bio="Premium handcrafted jewelry since 1990", 
                    address="Riyadh, Al-Olaya District", phone="0111234567", 
                    email="alsayed@jewelry.com", rating=Decimal("4.8")),
            Jeweler(name="Noura Diamonds", shop_name="Noura Luxury", 
                    bio="Exclusive diamond and gemstone designs", 
                    address="Jeddah, Al-Andalus Street", phone="0121234567", 
                    email="noura@jewelry.com", rating=Decimal("4.9")),
            Jeweler(name="Golden Craft", shop_name="Golden Craft Studio", 
                    bio="Traditional and modern gold craftsmanship", 
                    address="Dammam, King Fahd Road", phone="0131234567", 
                    email="goldencraft@jewelry.com", rating=Decimal("4.7")),
        ]
        for jeweler in jewelers:
            db.add(jeweler)
        db.commit()
        
        print("Seeding Categories...")
        categories = [
            Category(name="Rings", parent_id=None),
            Category(name="Necklaces", parent_id=None),
            Category(name="Bracelets", parent_id=None),
            Category(name="Earrings", parent_id=None),
            Category(name="Wedding Rings", parent_id=1),
            Category(name="Engagement Rings", parent_id=1),
            Category(name="Gold Chains", parent_id=2),
            Category(name="Diamond Necklaces", parent_id=2),
        ]
        for category in categories:
            db.add(category)
        db.commit()
        
        print("Seeding Payment Methods...")
        payment_methods = [
            PaymentMethod(method_name="Bank Transfer", 
                         qr_code_image="/static/uploads/bank_qr.png",
                         notes="SA0380000000608010167519 - Al-Rajhi Bank",
                         is_active=True),
            PaymentMethod(method_name="Apple Pay",
                         notes="Available for iOS users",
                         is_active=True),
            PaymentMethod(method_name="Credit Card",
                         notes="Visa, Mastercard accepted",
                         is_active=True),
        ]
        for method in payment_methods:
            db.add(method)
        db.commit()
        
        print("Seeding Products...")
        products_data = [
            {"jeweler_id": 1, "name": "Classic Gold Ring", "material": "Gold", "karat": "21K", 
             "weight": Decimal("5.5"), "price": Decimal("2500"), "stock_quantity": 10,
             "description": "Elegant classic gold ring for everyday wear", "image_path": "/static/products/ring1.jpg"},
            
            {"jeweler_id": 1, "name": "Diamond Engagement Ring", "material": "Gold", "karat": "18K", 
             "weight": Decimal("4.2"), "price": Decimal("8500"), "stock_quantity": 5,
             "description": "Stunning diamond engagement ring with VS1 clarity diamond", "image_path": "/static/products/ring2.jpg"},
            
            {"jeweler_id": 2, "name": "Ruby Heart Necklace", "material": "Gold", "karat": "18K", 
             "weight": Decimal("8.5"), "price": Decimal("12000"), "stock_quantity": 3,
             "description": "Beautiful heart-shaped ruby pendant with diamond halo", "image_path": "/static/products/necklace1.jpg"},
            
            {"jeweler_id": 2, "name": "Diamond Tennis Bracelet", "material": "White Gold", "karat": "18K", 
             "weight": Decimal("12.0"), "price": Decimal("15000"), "stock_quantity": 4,
             "description": "Classic tennis bracelet with 2 carat total diamond weight", "image_path": "/static/products/bracelet1.jpg"},
            
            {"jeweler_id": 3, "name": "Traditional Saudi Earrings", "material": "Gold", "karat": "21K", 
             "weight": Decimal("15.0"), "price": Decimal("6800"), "stock_quantity": 6,
             "description": "Traditional Saudi style earrings with intricate filigree work", "image_path": "/static/products/earrings1.jpg"},
            
            {"jeweler_id": 1, "name": "Pearl Drop Necklace", "material": "Silver", "karat": "925", 
             "weight": Decimal("6.5"), "price": Decimal("1800"), "stock_quantity": 15,
             "description": "Elegant freshwater pearl drop necklace", "image_path": "/static/products/necklace2.jpg"},
            
            {"jeweler_id": 2, "name": "Sapphire Ring", "material": "Platinum", "karat": "950", 
             "weight": Decimal("7.2"), "price": Decimal("22000"), "stock_quantity": 2,
             "description": "Rare blue sapphire ring with diamond accents", "image_path": "/static/products/ring3.jpg"},
            
            {"jeweler_id": 3, "name": "Gold Bangle Set", "material": "Gold", "karat": "21K", 
             "weight": Decimal("25.0"), "price": Decimal("11500"), "stock_quantity": 8,
             "description": "Set of 4 traditional gold bangles", "image_path": "/static/products/bracelet2.jpg"},
            
            {"jeweler_id": 1, "name": "Emerald Stud Earrings", "material": "Gold", "karat": "18K", 
             "weight": Decimal("3.5"), "price": Decimal("9500"), "stock_quantity": 7,
             "description": "Colombian emerald stud earrings", "image_path": "/static/products/earrings2.jpg"},
            
            {"jeweler_id": 2, "name": "Diamond Wedding Band", "material": "Platinum", "karat": "950", 
             "weight": Decimal("5.8"), "price": Decimal("11000"), "stock_quantity": 4,
             "description": "Eternity wedding band with channel-set diamonds", "image_path": "/static/products/ring4.jpg"},
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)
        db.commit()
        
        print("Assigning categories to products...")
        for i, product in enumerate(db.query(Product).all(), 1):
            if i <= 3:
                product.categories.append(db.query(Category).filter(Category.id == 1).first())
            elif i <= 5:
                product.categories.append(db.query(Category).filter(Category.id == 2).first())
            elif i <= 7:
                product.categories.append(db.query(Category).filter(Category.id == 3).first())
            else:
                product.categories.append(db.query(Category).filter(Category.id == 4).first())
        db.commit()
        
        print("Creating carts for users...")
        from models import Cart
        for user in db.query(User).all():
            cart = Cart(user_id=user.id)
            db.add(cart)
        db.commit()
        
        print("✅ Database seeded successfully!")
        
    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    seed_database()