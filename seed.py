from models import Category, Supplier, Product, StockMovement
from crud import (
    create_category, 
    create_supplier, 
    create_product, 
    create_stock_movement
)

def seed_database():
    print("Запуск заполнения базы тестовыми данными")
    
    try:
        cats = ["Электроника", "Канцелярия", "Мебель"]
        cat_ids = {}
        for name in cats:
            cat = create_category(name)
            if cat:
                cat_ids[name] = cat.id
                print(f"Создана категория: {name} (ID: {cat.id})")
            else:
                print(f"Не удалось создать категорию: {name}")

        suppliers_data = [
            ("ООО 'ТехноИмпорт'", "+79001112233", "tech@import.ru"),
            ("ИП Иванов", "+79004445566", "ivan@mail.ru"),
            ("Фабрика 'Комфорт'", "+79007778899", "mebel@comfort.ru")
        ]
        sup_ids = {}
        for name, phone, email in suppliers_data:
            sup = create_supplier(name, phone, email)
            if sup:
                sup_ids[name] = sup.id
                print(f"Создан поставщик: {name}")
            else:
                print(f"Не удалось создать поставщика: {name}")

        products_data = [
            ("Ноутбук ASUS", "NB-001", cat_ids["Электроника"], sup_ids["ООО 'ТехноИмпорт'"], 60000, 75000, 5),
            ("Мышь беспроводная", "MS-005", cat_ids["Электроника"], sup_ids["ООО 'ТехноИмпорт'"], 1500, 2500, 10),
            ("Блокнот А5", "BN-100", cat_ids["Канцелярия"], sup_ids["ИП Иванов"], 200, 400, 50),
            ("Кресло офисное", "CH-500", cat_ids["Мебель"], sup_ids["Фабрика 'Комфорт'"], 12000, 16000, 3),
        ]

        prod_ids = []
        for name, sku, cat_id, sup_id, purchase, selling, min_qty in products_data:
            prod = create_product(name, sku, cat_id, sup_id, purchase, selling, min_qty)
            if prod:
                prod_ids.append(prod.id)
                print(f"Создан товар: {name}")
            else:
                print(f"Не удалось создать товар: {name}")

        if prod_ids:
            print("  ✓ Добавление операций по складу...")
            create_stock_movement(prod_ids[0], "IN", 10, "Поступление ноутбуков")
            create_stock_movement(prod_ids[0], "OUT", 8, "Продажа ноутбуков")
            create_stock_movement(prod_ids[1], "IN", 20, "Поступление мышей")
            create_stock_movement(prod_ids[2], "ADJUST", -5, "Списание брака блокнотов")

        print("\nТестовые данные успешно добавлены!")

    except Exception as e:
        print(f"\nПроизошла критическая ошибка при заполнении: {e}")

seed_database()

