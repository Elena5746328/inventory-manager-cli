from crud import (
    create_category, get_all_categories,
    create_supplier, get_all_suppliers, deactivate_supplier,
    create_product, get_all_products, get_product_by_id,
    update_product_prices, deactivate_product,
    create_stock_movement,
)
from reports import (
    get_movements_history,
    get_movements_by_product,
    get_current_stock_report,
    get_low_stock_products,
    get_total_purchase_value,
    get_products_by_category,
    get_products_by_supplier       
)

def show_main_menu():
    print("\n" + "="*60)
    print("INVENTORY MANAGER CLI")
    print("="*60)
    print("1.  Создать категорию")
    print("2.  Показать все категории")
    print("3.  Создать поставщика")
    print("4.  Показать всех поставщиков")
    print("5.  Деактивировать поставщика")
    print("6.  Создать товар")
    print("7.  Показать все товары")
    print("8.  Показать товар по ID")
    print("9.  Обновить цену товара")
    print("10. Деактивировать товар")
    print("11. Добавить поступление товара (IN)")
    print("12. Добавить списание товара (OUT)")
    print("13. Добавить корректировку остатка (ADJUST)")
    print("14. Показать историю операций (все)")
    print("15. Показать операции по товару (по ID)")
    print("16. Показать текущие остатки")
    print("17. Показать товары, которые заканчиваются")
    print("18. Показать общую стоимость склада")
    print("19. Показать товары по категориям")
    print("20. Показать товары по поставщикам")
    print("0.  Выход")
    print("-"*60)

def main():
    while True:
        show_main_menu()
        choice = input("Выберите пункт меню (0-20): ").strip()

        try:
            if choice == "1":
                name = input("Название категории: ").strip()
                if name:
                    create_category(name)
                else:
                    print("Название не может быть пустым.")

            elif choice == "2":
                get_all_categories()

            elif choice == "3":
                name = input("Название поставщика: ").strip()
                phone = input("Телефон: ").strip()
                email = input("Email: ").strip()
                create_supplier(name, phone, email)

            elif choice == "4":
                get_all_suppliers()

            elif choice == "5":
                get_all_suppliers()
                sup_id = int(input("Введите ID поставщика для деактивации: "))
                deactivate_supplier(sup_id)

            elif choice == "6":
                name = input("Название товара: ").strip()
                sku = input("Артикул (SKU): ").strip()
                cat_id = int(input("ID категории: "))
                sup_id = int(input("ID поставщика: "))
                purchase_price = float(input("Закупочная цена: "))
                selling_price = float(input("Продажная цена: "))
                min_qty = int(input("Минимальный остаток: "))
                
                create_product(name, sku, cat_id, sup_id, purchase_price, selling_price, min_qty)

            elif choice == "7":
                get_all_products()

            elif choice == "8":
                prod_id = int(input("Введите ID товара: "))
                product = get_product_by_id(prod_id)
                if product:
                    status = "Активен" if product.is_active else "Неактивен"
                    print(f"Товар: {product.name} | SKU: {product.sku} | Цена: {product.selling_price} | Статус: {status}")
                else:
                    print("Товар не найден.")

            elif choice == "9":
                prod_id = int(input("ID товара: "))
                new_purchase = float(input("Новая закупочная цена: "))
                new_selling = float(input("Новая продажная цена: "))
                update_product_prices(prod_id, new_purchase, new_selling)

            elif choice == "10":
                prod_id = int(input("ID товара для деактивации: "))
                deactivate_product(prod_id)

            elif choice in ["11", "12", "13"]:
                prod_id = int(input("ID товара: "))
                qty = float(input("Количество: "))
                comment = input("Комментарий (опционально): ").strip()
                
                m_type = "IN" if choice == "11" else ("OUT" if choice == "12" else "ADJUST")
                create_stock_movement(prod_id, m_type, qty, comment)

            elif choice == "14":
                get_movements_history()

            elif choice == "15":
                prod_id = int(input("Введите ID товара для просмотра операций: "))
                get_movements_by_product(prod_id)

            elif choice == "16":
                get_current_stock_report()

            elif choice == "17":
                get_low_stock_products()

            elif choice == "18":
                get_total_purchase_value()

            elif choice == "19":
                get_products_by_category()

            elif choice == "20":
                get_products_by_supplier()

            elif choice == "0":
                print("До свидания!")
                break
            
            else:
                print("Неверный выбор. Введите число от 0 до 20.")

        except ValueError:
            print("Ошибка ввода: пожалуйста, вводите корректные числа там, где это требуется (ID, цены, количество).")
        except Exception as e:
            print(f"Произошла ошибка: {e}")

main()
