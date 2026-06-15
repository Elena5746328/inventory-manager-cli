from sqlalchemy import (
    Column, 
    Integer,
    String,
    Numeric,
    Float,
    DateTime,
    ForeignKey
)

from datetime import date
from typing import Optional
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column, relationship
from database import Base

class Category(Base):
    __tablename__ = "categories"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(100), nullable=False, unique=True)

    products = relationship("Product", back_populates="category")

class Supplier(Base):
    __tablename__ = "suppliers"

    id:Mapped[int] = mapped_column(Integer, primary_key=True)
    name:Mapped[str] = mapped_column(String(255), nullable=False, unique=True)
    phone:Mapped[str] = mapped_column(String(20))
    email: Mapped[int] = mapped_column(String(255), unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[] = mapped_column(DateTime, nullable=False)
    
class Product(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[int] = mapped_column(String(255), nullable=False)
    sku: Mapped[int] = mapped_column(String(50), nullable=False, unique=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey('categories.id'), nullable=False)
    supplier_id: Mapped[int] = mapped_column(Integer, ForeignKey('suppliers.id'), nullable=False)
    purchase_price: Mapped[int] = mapped_column(Numeric(12,2), nullable=False, default=0.0)
    selling_price: Mapped[int] = mapped_column(Numeric(12,2), nullable=False, default=0.0)
    min_quantity: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    created_at: Mapped[bool] = mapped_column(DateTime, nullable=False)

    category = relationship("Category", back_populates="products")
    supplier = relationship("Supplier", back_populates="products")
    stock_movements = relationship("StockMovement", back_populates="product")

class StockMovement(Base):
    __tablename__ = "stock_movements"
    __table_args__ = (
        CheckConstraint("movement_type IN ('IN', 'OUT', 'ADJUST')", name="check_movement_type"),
        CheckConstraint("quantity > 0", name="check_quantity_positive"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("products.id"), nullable=False)
    movement_type: Mapped[int] = mapped_column(String(10), nullable=False)
    quantity: Mapped[int] = mapped_column(Numeric(12,2), nullable=False)
    comment: Mapped[bool] = mapped_column(String(255))
    created_at: Mapped[] = mapped_column(DateTime, nullable=False)

    product = relationship("Product", back_populates="stock_movements")


    

    