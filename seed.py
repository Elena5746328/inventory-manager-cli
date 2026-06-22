from database import get_db
from crud import create_category, create_supplier, create_product, create_stock_movement

def seed_data():
    print("Заполнение тестовыми данными...")

    # Создаём категории
    category1 = create_category("Электроника")
    category2 = create_category("Канцтовары")

    # Создаём поставщиков
    supplier1 = create_supplier("ООО ТехСнаб", "8-800-123-45-67", "tech@mail.ru")
    supplier2 = create_supplier("КанцМир", "8-800-765-43-21", "kanc@mail.ru")

    # Создаём товары
    product1 = create_product(
        "Ноутбук ASUS", "NB-ASUS-001", category1.id, supplier1.id, 45000, 55000, 5
    )
    product2 = create_product(
        "Мышь беспроводная", "MOUSE-WIRELESS-002", category1.id, supplier1.id, 1500, 2500, 10
    )
    product3 = create_product(
        "Ручка шариковая", "PEN-BALL-003", category2.id, supplier2.id, 20, 50, 100
    )

    # Добавляем складские операции
    create_stock_movement(product1.id, "IN", 10, "Первая поставка")
    create_stock_movement(product2.id, "IN", 50, "Поставка мышей")
    create_stock_movement(product3.id, "IN", 200, "Поставка ручек")
    create_stock_movement(product1.id, "OUT", 2, "Продажа 2 ноутбуков")
    create_stock_movement(product2.id, "OUT", 15, "Продажа мышей")

    print("Тестовые данные успешно созданы!")

seed_data()