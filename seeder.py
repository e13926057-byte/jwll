import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from database import engine, SessionLocal, Base
from models.models import User, Jeweler, PaymentMethod, Category, Product, ProductCategory
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def seed_database():
    print("Starting database seeding...")
    
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        print("Creating users...")
        hashed_password = pwd_context.hash("password123")
        
        users = [
            User(
                username="admin",
                email="admin@jewelry.com",
                password=hashed_password,
                first_name="Admin",
                last_name="User",
                phone="+966501234567",
                gender="male",
                created_at=datetime.utcnow()
            ),
            User(
                username="user1",
                email="user1@example.com",
                password=hashed_password,
                first_name="أحمد",
                last_name="محمد",
                phone="+966501234568",
                gender="male",
                created_at=datetime.utcnow()
            ),
            User(
                username="user2",
                email="user2@example.com",
                password=hashed_password,
                first_name="سارة",
                last_name="علي",
                phone="+966501234569",
                gender="female",
                created_at=datetime.utcnow()
            ),
            User(
                username="user3",
                email="user3@example.com",
                password=hashed_password,
                first_name="خالد",
                last_name="أحمد",
                phone="+966501234570",
                gender="male",
                created_at=datetime.utcnow()
            ),
            User(
                username="user4",
                email="user4@example.com",
                password=hashed_password,
                first_name="نورة",
                last_name="عبدالله",
                phone="+966501234571",
                gender="female",
                created_at=datetime.utcnow()
            ),
        ]
        for user in users:
            db.add(user)
        db.commit()
        for user in users:
            db.refresh(user)
        
        print("Creating jewelers...")
        jewelers = [
            Jeweler(
                user_id=users[0].id,
                name="أحمد الذهبي",
                shop_name="محل الذهبي للمجوهرات",
                bio="أفضل محلات المجوهرات في المملكة",
                address="الرياض، شارع العليا",
                phone="+966112345678",
                email="jeweler1@jewelry.com",
                rating=4.8,
                created_at=datetime.utcnow()
            ),
            Jeweler(
                user_id=users[1].id,
                name="محمد الفضة",
                shop_name="محل الفضة للمجوهرات",
                bio="تصاميم فريدة من الفضة والذهب",
                address="جدة، شارع التحلية",
                phone="+966122345678",
                email="jeweler2@jewelry.com",
                rating=4.5,
                created_at=datetime.utcnow()
            ),
            Jeweler(
                user_id=users[2].id,
                name="عبداللهالماس",
                shop_name="محل الماس للألماس",
                bio="ألماس طبيعي عالي الجودة",
                address="الدمام، شارع الاستقلال",
                phone="+966132345678",
                email="jeweler3@jewelry.com",
                rating=4.9,
                created_at=datetime.utcnow()
            ),
        ]
        for jeweler in jewelers:
            db.add(jeweler)
        db.commit()
        for jeweler in jewelers:
            db.refresh(jeweler)
        
        print("Creating payment methods...")
        payment_methods = [
            PaymentMethod(
                method_name="Bank Transfer",
                qr_code_image="/static/qr/bank_transfer.png",
                is_active=True,
                notes="تحويل بنكي إلى حساب البنك الأهلي"
            ),
            PaymentMethod(
                method_name="Cash on Delivery",
                qr_code_image=None,
                is_active=True,
                notes="دفع عند الاستلام"
            ),
        ]
        for pm in payment_methods:
            db.add(pm)
        db.commit()
        
        print("Creating categories...")
        categories = [
            Category(name="خواتم", parent_id=None),
            Category(name="قلائد", parent_id=None),
            Category(name="أقراط", parent_id=None),
            Category(name="أساور", parent_id=None),
            Category(name="خواتم ذهب", parent_id=1),
            Category(name="خواتم فضة", parent_id=1),
            Category(name="قلائد ذهب", parent_id=2),
            Category(name="قلائد فضة", parent_id=2),
        ]
        for cat in categories:
            db.add(cat)
        db.commit()
        for cat in categories:
            db.refresh(cat)
        
        print("Creating products...")
        products = [
            Product(
                jeweler_id=jewelers[0].id,
                name="خاتم ذهبي عيار 21",
                material="ذهب",
                karat="21k",
                weight=8.5,
                price=2500.00,
                stock_quantity=15,
                description="خاتم ذهبي عيار 21 بتصميم عصري",
                image_path="/static/products/ring1.jpg"
            ),
            Product(
                jeweler_id=jewelers[0].id,
                name="قلادة ذهبية مرصعة",
                material="ذهب",
                karat="18k",
                weight=15.0,
                price=4500.00,
                stock_quantity=8,
                description="قلادة ذهبية مرصعة بالألماس",
                image_path="/static/products/necklace1.jpg"
            ),
            Product(
                jeweler_id=jewelers[1].id,
                name="أقراط فضية بتصميم كلاسيكي",
                material="فضة",
                karat="925",
                weight=5.0,
                price=350.00,
                stock_quantity=25,
                description="أقراط فضية925 بتصميم كلاسيكي أنيق",
                image_path="/static/products/earring1.jpg"
            ),
            Product(
                jeweler_id=jewelers[1].id,
                name="سوار فضي مرصع",
                material="فضة",
                karat="925",
                weight=12.0,
                price=500.00,
                stock_quantity=20,
                description="سوار فضي مرصع بالأحجار الكريمة",
                image_path="/static/products/bracelet1.jpg"
            ),
            Product(
                jeweler_id=jewelers[2].id,
                name="خاتم ألماس كلاسيك",
                material="ذهب",
                karat="18k",
                weight=6.0,
                price=8500.00,
                stock_quantity=5,
                description="خاتم ألماس كلاسيك بحجر 1 قيراط",
                image_path="/static/products/ring2.jpg"
            ),
            Product(
                jeweler_id=jewelers[2].id,
                name="قلادة ياقوت",
                material="ذهب",
                karat="21k",
                weight=20.0,
                price=12000.00,
                stock_quantity=3,
                description="قلادة ياقوت أحمر طبيعي مرصعة بالألماس",
                image_path="/static/products/necklace2.jpg"
            ),
            Product(
                jeweler_id=jewelers[0].id,
                name="خاتم زفاف ذهبي",
                material="ذهب",
                karat="21k",
                weight=10.0,
                price=3200.00,
                stock_quantity=30,
                description="خاتم زفاف ذهبي عيار 21 بتصميم رومانسي",
                image_path="/static/products/ring3.jpg"
            ),
            Product(
                jeweler_id=jewelers[1].id,
                name="أقراط ذهبية dangling",
                material="ذهب",
                karat="18k",
                weight=8.0,
                price=1800.00,
                stock_quantity=12,
                description="أقراط ذهبية dangling بتصميم أنيق",
                image_path="/static/products/earring2.jpg"
            ),
            Product(
                jeweler_id=jewelers[2].id,
                name="سوار ذهبي رفيع",
                material="ذهب",
                karat="21k",
                weight=25.0,
                price=7500.00,
                stock_quantity=10,
                description="سوار ذهبي رفيع بتصميم عصري",
                image_path="/static/products/bracelet2.jpg"
            ),
            Product(
                jeweler_id=jewelers[0].id,
                name="قلادة اسم شخصية",
                material="ذهب",
                karat="18k",
                weight=5.0,
                price=1500.00,
                stock_quantity=50,
                description="قلادة ذهبية باسمك الشخصي",
                image_path="/static/products/necklace3.jpg"
            ),
        ]
        for product in products:
            db.add(product)
        db.commit()
        for product in products:
            db.refresh(product)
        
        print("Linking products to categories...")
        product_categories = [
            ProductCategory(product_id=products[0].id, category_id=1),
            ProductCategory(product_id=products[0].id, category_id=5),
            ProductCategory(product_id=products[1].id, category_id=2),
            ProductCategory(product_id=products[1].id, category_id=7),
            ProductCategory(product_id=products[2].id, category_id=3),
            ProductCategory(product_id=products[2].id, category_id=8),
            ProductCategory(product_id=products[3].id, category_id=4),
            ProductCategory(product_id=products[3].id, category_id=8),
            ProductCategory(product_id=products[4].id, category_id=1),
            ProductCategory(product_id=products[4].id, category_id=5),
            ProductCategory(product_id=products[5].id, category_id=2),
            ProductCategory(product_id=products[5].id, category_id=7),
            ProductCategory(product_id=products[6].id, category_id=1),
            ProductCategory(product_id=products[6].id, category_id=5),
            ProductCategory(product_id=products[7].id, category_id=3),
            ProductCategory(product_id=products[7].id, category_id=7),
            ProductCategory(product_id=products[8].id, category_id=4),
            ProductCategory(product_id=products[8].id, category_id=5),
            ProductCategory(product_id=products[9].id, category_id=2),
            ProductCategory(product_id=products[9].id, category_id=7),
        ]
        for pc in product_categories:
            db.add(pc)
        db.commit()
        
        print("Database seeding completed successfully!")
        print(f"Created: {len(users)} users, {len(jewelers)} jewelers, {len(payment_methods)} payment methods, {len(categories)} categories, {len(products)} products")
        
    except Exception as e:
        print(f"Error during seeding: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
