from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional, List
from database import get_db
from models.models import Product, ProductImage, Category, ProductCategory
from schemas.schemas import (
    ProductCreate, ProductUpdate, ProductResponse,
    CategoryCreate, CategoryResponse
)
from routers.auth import get_current_user
from models.models import User

router = APIRouter(prefix="/api", tags=["المتجر"])


@router.get("/products", response_model=List[ProductResponse])
def get_products(
    category_id: Optional[int] = None,
    material: Optional[str] = None,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Product)
    
    if category_id:
        query = query.join(ProductCategory).filter(ProductCategory.category_id == category_id)
    
    if material:
        query = query.filter(Product.material.ilike(f"%{material}%"))
    
    if min_price is not None:
        query = query.filter(Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(Product.price <= max_price)
    
    products = query.all()
    return products


@router.get("/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="المنتج غير موجود")
    return product


@router.post("/products", response_model=ProductResponse)
def create_product(
    product: ProductCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_product = Product(
        name=product.name,
        jeweler_id=product.jeweler_id,
        material=product.material,
        karat=product.karat,
        weight=product.weight,
        price=product.price,
        stock_quantity=product.stock_quantity,
        description=product.description,
        image_path=product.image_path
    )
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    if product.category_ids:
        for cat_id in product.category_ids:
            pc = ProductCategory(product_id=new_product.id, category_id=cat_id)
            db.add(pc)
        db.commit()
    
    return new_product


@router.put("/products/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product: ProductUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="المنتج غير موجود")
    
    update_data = product.dict(exclude_unset=True)
    category_ids = update_data.pop("category_ids", None)
    
    for key, value in update_data.items():
        setattr(db_product, key, value)
    
    if category_ids is not None:
        db.query(ProductCategory).filter(ProductCategory.product_id == product_id).delete()
        for cat_id in category_ids:
            pc = ProductCategory(product_id=product_id, category_id=cat_id)
            db.add(pc)
    
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="المنتج غير موجود")
    
    db.query(ProductCategory).filter(ProductCategory.product_id == product_id).delete()
    db.query(ProductImage).filter(ProductImage.product_id == product_id).delete()
    db.delete(product)
    db.commit()
    return {"message": "تم حذف المنتج بنجاح"}


@router.get("/categories", response_model=List[CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    categories = db.query(Category).all()
    return categories


@router.post("/categories", response_model=CategoryResponse)
def create_category(
    category: CategoryCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    new_category = Category(name=category.name, parent_id=category.parent_id)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category


@router.delete("/categories/{category_id}")
def delete_category(
    category_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    category = db.query(Category).filter(Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="الفئة غير موجودة")
    
    db.query(ProductCategory).filter(ProductCategory.category_id == category_id).delete()
    db.delete(category)
    db.commit()
    return {"message": "تم حذف الفئة بنجاح"}
