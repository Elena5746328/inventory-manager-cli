from database import get_db
from models import Product, Category, Supplier, StockMovement
from sqlalchemy import func, case
from decimal import Decimal


