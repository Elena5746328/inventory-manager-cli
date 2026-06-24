from database import SessionLocal
from models import Product, Category, Supplier, StockMovement

def calculate_all_stocks():
    db = SessionLocal()
    moves = db.query(StockMovement).all()
    
    stock = {}
    for m in moves:
        if m.product_id not in stock:
            stock[m.product_id] = 0
        
        if m.movement_type == "IN":
            stock[m.product_id] += m.quantity
        elif m.movement_type == "OUT":
            stock[m.product_id] -= m.quantity
        elif m.movement_type == "ADJUST":
            stock[m.product_id] += m.quantity
            
    return stock

def get_movements_history():
    db = SessionLocal()
    results = db.query(StockMovement).order_by(StockMovement.created_at.desc()).all()
    
    print("\nИСТОРИЯ ВСЕХ ОПЕРАЦИЙ")
    print("-" * 80)
    if not results:
        print("Нет операций.")
        return
    
    for row in results:
        prod_name = row.product.name if row.product else "[Товар удалён]"
        print(f"[{row.created_at}] | Товар: {prod_name:<20} | Тип: {row.movement_type:<5} | "
              f"Кол-во: {row.quantity} | {row.comment}")


def get_movements_by_product(product_id):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        print("Товар с таким ID не найден.")
        return

    results = (db.query(StockMovement)
               .filter(StockMovement.product_id == product_id)
               .order_by(StockMovement.created_at.desc())
               .all())
    
    print(f"\nОПЕРАЦИИ ПО ТОВАРУ: '{product.name}' (ID: {product_id})")
    print("-" * 80)
    if not results:
        print("По этому товару нет операций.")
        return
        
    for row in results:
        print(f"[{row.created_at}] | Тип: {row.movement_type:<5} | Кол-во: {row.quantity} | {row.comment}")


def get_current_stock_report():
    db = SessionLocal()
    products = db.query(Product).all()
    stocks = calculate_all_stocks()
    
    print("\nТЕКУЩИЕ ОСТАТКИ")
    print("-" * 60)
    if not products:
        print("Нет товаров.")
        return
        
    for prod in products:
        qty = stocks.get(prod.id, 0)
        print(f"{prod.name:<25} | Остаток: {qty}")


def get_low_stock_products():
    db = SessionLocal()
    products = db.query(Product).filter(Product.is_active == True).all()
    stocks = calculate_all_stocks()
    
    print("\nТОВАРЫ, КОТОРЫЕ ЗАКАНЧИВАЮТСЯ")
    print("-" * 60)
    found = False
    
    for prod in products:
        qty = stocks.get(prod.id, 0)
        if qty < prod.min_quantity:
            found = True
            needed = prod.min_quantity - qty
            print(f"{prod.name:<25} | Мин: {prod.min_quantity} | Сейчас: {qty} | Нужно: {needed}")
    
    if not found:
        print("Все товары в норме!")


def get_total_purchase_value():
    db = SessionLocal()
    products = db.query(Product).filter(Product.is_active == True).all()
    stocks = calculate_all_stocks()
    
    total = 0
    for prod in products:
        qty = stocks.get(prod.id, 0)
        total += qty * prod.purchase_price

    print(f"\nОБЩАЯ ЗАКУПОЧНАЯ СТОИМОСТЬ: {total} руб.")

def get_products_by_category():
    db = SessionLocal()
    categories = db.query(Category).all()

def get_products_by_category():
    db = SessionLocal()
    categories = db.query(Category).all()

    print("\nТОВАРЫ ПО КАТЕГОРИЯМ")
    print("-" * 60)
    
    if not categories:
        print("Нет категорий.")
        return

    for cat in categories:
        products = db.query(Product).filter(
            Product.category_id == cat.id, 
            Product.is_active == True
        ).all()
        
        if products:
            print(f"\nКатегория: {cat.name}")
            for prod in products:
                print(f"   - {prod.name} (SKU: {prod.sku})")
        else:
            print(f"\nКатегория: {cat.name} — активных товаров нет.")

def get_products_by_supplier():
    db = SessionLocal()
    suppliers = db.query(Supplier).all()
    
    print("\nТОВАРЫ ПО ПОСТАВЩИКАМ")
    print("-" * 60)
    
    if not suppliers:
        print("Нет поставщиков.")
        return

    for sup in suppliers:
        products = db.query(Product).filter(
            Product.supplier_id == sup.id, 
            Product.is_active == True
        ).all()
        
        if products:
            print(f"\nПоставщик: {sup.name}")
            for prod in products:
                print(f"   - {prod.name} (SKU: {prod.sku})")
        else:
            print(f"\nПоставщик: {sup.name} — активных товаров нет.")
