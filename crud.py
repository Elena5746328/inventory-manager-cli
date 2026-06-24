from database import SessionLocal
from models import Category, Supplier, Product, StockMovement
from decimal import Decimal
from sqlalchemy.exc import IntegrityError

def create_category(name: str): 
    db = SessionLocal()
    try:
        category = Category(name=name)
        db.add(category)
        db.commit()
        db.refresh(category)
        print(f"Категория '{name}' создана с ID: {category.id}")
        return category
    except IntegrityError:
        db.rollback()
        print(f"Ошибка: категория '{name}' уже существует.")
        return None

def get_all_categories():
    db = SessionLocal()
    categories = db.query(Category).all()
    if not categories:
        print("Категории не найдены.")
    else:
        print("\nВсе категории:")
        for cat in categories:
            print(f"{cat.id}. {cat.name}")
    return categories

def get_category_by_id(category_id: int):
    db = SessionLocal()
    category = db.query(Category).filter(Category.id == category_id).first()
    return category

def update_category_name(category_id: int, new_name: str):
    db = SessionLocal()
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            category.name = new_name
            db.commit()
            print(f"Название категории обновлено на '{new_name}'")
        else:
            print("Категория не найдена.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка обновления: {e}")

def delete_category(category_id: int):
    db = SessionLocal()
    try:
        category = db.query(Category).filter(Category.id == category_id).first()
        if category:
            db.delete(category)
            db.commit()
            print(f"Категория с ID {category_id} удалена.")
        else:
            print("Категория не найдена.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка удаления: {e}")

def create_supplier(name: str, phone: str = None, email: str = None):
    db = SessionLocal()
    try:
        supplier = Supplier(name=name, phone=phone, email=email)
        db.add(supplier)
        db.commit()
        db.refresh(supplier)
        print(f"Поставщик '{name}' создан с ID: {supplier.id}")
        return supplier
    except IntegrityError:
        db.rollback()
        print(f"Ошибка: поставщик '{name}' уже существует.")
        return None

def get_all_suppliers():
    db = SessionLocal()
    suppliers = db.query(Supplier).all()
    if not suppliers:
        print("Поставщики не найдены.")
    else:
        print("\nВсе поставщики:")
        for sup in suppliers:
            status = "Активен" if sup.is_active else "Неактивен"
            print(
                f"{sup.id}. {sup.name} | "
                f"Телефон: {sup.phone or 'Не указан'} | "
                f"Email: {sup.email or 'Не указан'} | "
                f"Статус: {status}"
            )
    return suppliers

def deactivate_supplier(supplier_id: int):
    db = SessionLocal()
    try:
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if supplier:
            supplier.is_active = False
            db.commit()
            print(f"Поставщик '{supplier.name}' деактивирован.")
        else:
            print("Поставщик не найден.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка деактивации: {e}")

def delete_supplier(supplier_id: int):
    db = SessionLocal()
    try:
        supplier = db.query(Supplier).filter(Supplier.id == supplier_id).first()
        if supplier:
            db.delete(supplier)
            db.commit()
            print(f"Поставщик с ID {supplier_id} удалён.")
        else:
            print("Поставщик не найден.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка удаления: {e}")

def create_product(
    name: str, sku: str, category_id: int,
    supplier_id: int = None, purchase_price: Decimal = 0,
    selling_price: Decimal = 0, min_quantity: int = 0
):
    db = SessionLocal()
    try:
        product = Product(
            name=name, sku=sku, category_id=category_id,
            supplier_id=supplier_id, purchase_price=float(purchase_price),
            selling_price=float(selling_price), min_quantity=min_quantity
        )
        db.add(product)
        db.commit()
        db.refresh(product)
        print(f"Товар '{name}' создан с ID: {product.id}")
        return product
    except IntegrityError:
        db.rollback()
        print(f"Ошибка: товар с SKU '{sku}' уже существует.")
        return None

def get_all_products():
    db = SessionLocal()
    products = db.query(Product).all()
    if not products:
        print("Товары не найдены.")
    else:
        print("\nВсе товары:")
        for prod in products:
            print(
                f"{prod.id}. {prod.name} (SKU: {prod.sku}) | "
                f"Закупочная: {prod.purchase_price} | Продажная: {prod.selling_price} | "
                f"Мин. остаток: {prod.min_quantity} | Статус: {prod.is_active}"
            )
    return products

def get_product_by_id(product_id: int):
    db = SessionLocal()
    product = db.query(Product).filter(Product.id == product_id).first()
    return product

def get_products_by_category():
    db = SessionLocal()
    categories = db.query(Category).all()
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
                print(f"- {prod.name} (SKU: {prod.sku})")
        else:
            print(f"\nКатегория: {cat.name} — активных товаров нет.")

def get_products_by_supplier(supplier_id: int):
    db = SessionLocal()
    products = db.query(Product).filter(Product.supplier_id == supplier_id).all()
    if not products:
        print("Товары этого поставщика не найдены.")
    else:
        print(f"\nТовары поставщика ID {supplier_id}:")
        for prod in products:
            print(f"{prod.id}. {prod.name}")
    return products

def update_product_prices(product_id: int, purchase_price: Decimal, selling_price: Decimal):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.purchase_price = float(purchase_price)
            product.selling_price = float(selling_price)
            db.commit()
            print(f"Цены товара '{product.name}' обновлены.")
        else:
            print("Товар не найден.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка обновления цен: {e}")

def update_product_min_quantity(product_id: int, min_qty: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.min_quantity = min_qty
            db.commit()
            print(f"Минимальный остаток для '{product.name}' обновлён.")
        else:
            print("Товар не найден.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка обновления минимального остатка: {e}")

def deactivate_product(product_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.is_active = False
            db.commit()
            print(f"Товар '{product.name}' деактивирован.")
        else:
            print("Товар не найден.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка деактивации: {e}")

def delete_product(product_id: int):
    db = SessionLocal()
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            db.delete(product)
            db.commit()
            print(f"Товар с ID {product_id} удалён.")
        else:
            print("Товар не найден.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка удаления: {e}")

def create_stock_movement(product_id: int, movement_type: str, quantity: float, comment: str = None):
    db = SessionLocal()
    try:
        movement = StockMovement(
            product_id=product_id, movement_type=movement_type,
            quantity=quantity, comment=comment
        )
        db.add(movement)
        db.commit()
        db.refresh(movement)
        print(f"Операция '{movement_type}' для товара ID {product_id} создана.")
        return movement
    except Exception as e:
        db.rollback()
        print(f"Ошибка создания операции: {e}")
        return None

def get_all_stock_movements():
    db = SessionLocal()
    movements = db.query(StockMovement).all()
    if not movements:
        print("Складские операции не найдены.")
    else:
        print("\nИстория операций:")
        for move in movements:
            print(
                f"{move.id}. Товар ID {move.product_id} | "
                f"Тип: {move.movement_type} | Кол-во: {move.quantity} | "
                f"Дата: {move.created_at} | Комментарий: {move.comment or 'Без комментария'}"
            )
    return movements

def get_movements_by_product(product_id: int):
    db = SessionLocal()
    movements = db.query(StockMovement).filter(StockMovement.product_id == product_id).all()
    if not movements:
        print(f"Операции для товара ID {product_id} не найдены.")
    else:
        print(f"\nОперации для товара ID {product_id}:")
        for move in movements:
            print(
                f"{move.id}. Тип: {move.movement_type} | "
                f"Кол-во: {move.quantity} | Дата: {move.created_at} | "
                f"Комментарий: {move.comment or 'Без комментария'}"
            )
    return movements

def delete_stock_movement(movement_id: int):
    db = SessionLocal()
    try:
        movement = db.query(StockMovement).filter(StockMovement.id == movement_id).first()
        if movement:
            db.delete(movement)
            db.commit()
            print(f"Операция с ID {movement_id} удалена.")
        else:
            print("Операция не найдена.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка удаления операции: {e}")
