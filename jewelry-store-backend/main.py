from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from database import engine, Base
from routers import auth, products, carts, orders, categories, designs
import os

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Jewelry Store API",
    description="API for Jewelry E-commerce and AI Design Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("static/generated_designs", exist_ok=True)
os.makedirs("static/products", exist_ok=True)
os.makedirs("static/uploads", exist_ok=True)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(carts.router)
app.include_router(orders.router)
app.include_router(categories.router)
app.include_router(designs.router)

@app.get("/")
def read_root():
    return {
        "message": "مرحباً بك في API متجر المجوهرات",
        "docs": "/docs",
        "version": "1.0.0"
    }