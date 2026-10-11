

products = [
    {"id": 1, "name": "Клавіатура", "price": 899.99, "stock": 10},
    {"id": 2, "name": "Мишка", "price": 499.50, "stock": 15},
    {"id": 3, "name": "Навушники", "price": 1299.00, "stock": 7},
    {"id": 4, "name": "Килимок", "price": 199.99, "stock": 20}
]

cart = []

admin_login = "admin"
admin_password = "1234"

# Лямбда-функція для сортування товарів за назвою
sort_by_name = lambda product: product["name"]


def show_catalog():
    print("\n--- КАТАЛОГ ТОВАРІВ ---")
    for product in sorted(products, key=sort_by_name):
        print(
            product["id"], product["name"],
            "-", format(product["price"], ".2f"), "грн",
            "| Залишок:", product["stock"]
        )


def show_cart():
    print("\n--- КОШИК ---")

    if len(cart) == 0:
        print("Кошик порожній.")
        return

    total = 0

    for item in cart:
        for product in products:
            if product["id"] == item["id"]:
                price = product["price"] * item["quantity"]
                print(product["name"], "x", item["quantity"],
                      "-", format(price, ".2f"), "грн")
                total = total + price

    print("Разом:", format(total, ".2f"), "грн")


def add_to_cart():
    show_catalog()

    try:
        product_id = int(input("Введіть номер товару: "))
        quantity = int(input("Введіть кількість: "))
    except ValueError:
        print("Потрібно вводити числа.")
        return

    if quantity <= 0:
        print("Кількість має бути більшою за нуль.")
        return

    for product in products:
        if product["id"] == product_id:
            if quantity > product["stock"]:
                print("Недостатньо товару на складі.")
                return

            for item in cart:
                if item["id"] == product_id:
                    if item["quantity"] + quantity > product["stock"]:
                        print("Недостатньо товару на складі.")
                        return
                    item["quantity"] = item["quantity"] + quantity
                    print("Кількість товару оновлено.")
                    return

            cart.append({"id": product_id, "quantity": quantity})
            print("Товар додано в кошик.")
            return

    print("Товар не знайдено.")


def remove_from_cart():
    if len(cart) == 0:
        print("Кошик порожній.")
        return

    show_cart()

    try:
        product_id = int(input("Введіть номер товару для видалення: "))
    except ValueError:
        print("Потрібно ввести число.")
        return

    for item in cart:
        if item["id"] == product_id:
            cart.remove(item)
            print("Товар видалено з кошика.")
            return

    print("Такого товару в кошику немає.")


def buy_products():
    if len(cart) == 0:
        print("Кошик порожній.")
        return

    total = 0

    for item in cart:
        for product in products:
            if product["id"] == item["id"]:
                total = total + product["price"] * item["quantity"]

    for item in cart:
        for product in products:
            if product["id"] == item["id"]:
                product["stock"] = product["stock"] - item["quantity"]

    print("Покупку виконано!")
    print("До сплати:", format(total, ".2f"), "грн")
    cart.clear()


def admin_panel():
    login = input("Логін адміністратора: ")
    password = input("Пароль адміністратора: ")

    if login == admin_login and password == admin_password:
        print("\n--- ЗАЛИШКИ НА СКЛАДІ ---")

        # Лямбда-функція відбирає товари, які є в наявності
        available = list(filter(lambda product: product["stock"] > 0, products))

        for product in available:
            print(product["name"], "-", product["stock"], "шт.")

        for product in products:
            if product["stock"] == 0:
                print(product["name"], "- немає в наявності")
    else:
        print("Неправильний логін або пароль.")


def main():
    while True:
        print("\n--- МІНІМАГАЗИН ---")
        print("1. Переглянути каталог")
        print("2. Додати товар у кошик")
        print("3. Переглянути кошик")
        print("4. Видалити товар із кошика")
        print("5. Купити товари")
        print("6. Увійти як адміністратор")
        print("0. Вихід")

        choice = input("Ваш вибір: ")

        if choice == "1":
            show_catalog()
        elif choice == "2":
            add_to_cart()
        elif choice == "3":
            show_cart()
        elif choice == "4":
            remove_from_cart()
        elif choice == "5":
            buy_products()
        elif choice == "6":
            admin_panel()
        elif choice == "0":
            print("До побачення!")
            break
        else:
            print("Невірний пункт меню.")


main()
