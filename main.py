import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from database import engine, Base
from routers import auth, products, cart, orders, ai, design_requests, payment_methods

app = FastAPI(
    title="Jewelry E-commerce API",
    description="Backend API for Jewelry E-commerce and AI Design Platform",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

static_dir = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_dir):
    os.makedirs(static_dir)
generated_designs_dir = os.path.join(static_dir, "generated_designs")
if not os.path.exists(generated_designs_dir):
    os.makedirs(generated_designs_dir)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(auth.router)
app.include_router(products.router)
app.include_router(cart.router)
app.include_router(orders.router)
app.include_router(ai.router)
app.include_router(design_requests.router)
app.include_router(payment_methods.router)


@app.get("/")
def read_root():
    return {"message": "Welcome to Jewelry E-commerce API", "status": "running"}


@app.get("/health")
def health_check():
    return {"status": "healthy"}
