from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from services.auth import get_current_active_user
import models
import schemas

router = APIRouter(prefix="/api/products", tags=["Products"])

@router.get("/", response_model=List[schemas.ProductResponse])
def get_products(
    category_id: Optional[int] = Query(None),
    jeweler_id: Optional[int] = Query(None),
    material: Optional[str] = Query(None),
    min_price: Optional[float] = Query(None),
    max_price: Optional[float] = Query(None),
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    query = db.query(models.Product)
    
    if category_id:
        query = query.join(models.product_categories).filter(
            models.product_categories.c.category_id == category_id
        )
    
    if jeweler_id:
        query = query.filter(models.Product.jeweler_id == jeweler_id)
    
    if material:
        query = query.filter(models.Product.material == material)
    
    if min_price is not None:
        query = query.filter(models.Product.price >= min_price)
    
    if max_price is not None:
        query = query.filter(models.Product.price <= max_price)
    
    products = query.offset(skip).limit(limit).all()
    return products

@router.get("/{product_id}", response_model=schemas.ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=schemas.ProductResponse)
def create_product(
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_product = models.Product(**product.dict(exclude={'category_ids'}))
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    
    if product.category_ids:
        for cat_id in product.category_ids:
            category = db.query(models.Category).filter(models.Category.id == cat_id).first()
            if category:
                db_product.categories.append(category)
        db.commit()
    
    return db_product

@router.put("/{product_id}", response_model=schemas.ProductResponse)
def update_product(
    product_id: int,
    product: schemas.ProductCreate,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    for key, value in product.dict(exclude={'category_ids'}).items():
        setattr(db_product, key, value)
    
    if product.category_ids is not None:
        db_product.categories = []
        for cat_id in product.category_ids:
            category = db.query(models.Category).filter(models.Category.id == cat_id).first()
            if category:
                db_product.categories.append(category)
    
    db.commit()
    db.refresh(db_product)
    return db_product

@router.delete("/{product_id}")
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    current_user: models.User = Depends(get_current_active_user)
):
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db.delete(db_product)
    db.commit()
    return {"message": "Product deleted successfully"}