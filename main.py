from decimal import Decimal
from database import Base, engine
from crud import (
    create_category,
    create_supplier,
    create_product,
    create_stock_movement,
    deactivate_product,
    get_all_categories,
    get_all_suppliers,
    get_all_products,
    get_all_stock_movements
)

def show_main_menu():
    print("\n" + "="*50)
    print("Система управления складом:")
    print("="*50)
    print("1. Создать категорию")
    print("2. Показать все категории")
    print("3. Создать поставщика")
    print("4. Показать всех поставщиков")
    print("5. Деактивировать поставщика")
    print("6. Создать товар")
    print("7. Показать все товары")
    print("8. Показать товар по id")
    print("9. Обновить цену товара")
    print("10. Деактивировать товар")
    print("11. Добавить поступление товара")
    print("12. Добавить списание товара")
    print("13. Добавить корректировку остатка")
    print("14. Показать историю операций")
    print("15. Показать операции по товару")
    print("16. Показать текущие остатки")
    print("17. Показать товары, которые заканчиваются")
    print("18. Показать общую стоимость склада")
    print("19. Показать товары по категориям")
    print("20. Показать товары по поставщикам")
    print("0. Выход")

def main():
    while True:
        show_main_menu()
        choice = input("Выберите пункт меню(0-20): ")

        if choice == "1":
            name = input("Название категории: ")
            create_category()

        elif choice == "2":
            get_all_categories()

        elif choice == "3":
            cat_id = int(input("ID категории: "))
            category = get_category_by_id(cat_id)
            if category:
                print(f"Категория: {category.name}")
            else:
                print("Категория не найдена")
        
        elif choice == "4":
            name = input("Название поставщика: ")
            phone = input("Телефон: ")
            email = input("Email: ")

        elif choice == "5":
            get_all_suppliers()

        elif choice == "6":
            name = input("название товара: ")
            sku = input("Артикул (SKU): ")
            category_id = int(input("ID категории: "))
            supplier_id = int(input("ID поставщика: "))
            purchase_price = float(input("Закупочная цена: "))
            selling_price = float(input("Продажная цена: "))
            min_quantity = int(input("Минимальный остаток: "))

        elif choice == "7":
            get_all_products()

        elif choice == "8":
            prod_id = int(input("ID товара: "))
            product = get_product_by_id(prod_id)
            if product:
                print(f"Товар: {product.name}, Артикул: {product.sku}, Цена: {product.selling_price}")
            else:
                print("Товар не найден")

        elif choice == "9":
            product_id = int(input("ID товара: "))
            new_price = float(input("Новая закупочная цена: "))
        
        elif choice == "10":
            product_id = int(input("ID товара: "))
            new_min = int(input("Новое минимальное количество: "))

        elif choice == "11":
            product_id = int(input("ID товара для деактивации: "))
        
        elif choice == "12":
            product_id = int(input("ID товара для удаления: "))

        elif choice == "13":
            product_id = int(input("ID товара: "))
            quantity = float(input("Количество: "))
            comment = input("Комментарий (опционально): ")

        elif choice == "14":
            product_id = int(input("ID товара: "))
            quantity = float(input("Количество: "))
            comment = input("Комментарий (опционально): ")

        elif choice == "15":
            product_id = int(input("ID товара: "))
            quantity = float(input("Количество: "))
            comment = input("Комментарий (опционально): ")

        elif choice == "16":
            get_products_with_category_and_supplier()

        elif choice == "17":
            get_movements_with_product()

        elif choice == "18":
            get_low_stock_products()

        elif choice == "19":
            get_total_purchase_value()

        elif choice == "20":
            get_inventory_turnover_report()

        elif choice == "0":
            print("До свидания")
            break

        else: 
            print("Неверный выбор. Введите число от 0 до 20")
        
main()






