import random


# 1. Класи помилок
# Створюємо окремі помилки для різних ситуацій у грі.

class GameError(Exception):
    pass


class InventoryFullError(GameError):
    pass


class InsufficientIngredientsError(GameError):
    pass


class RecipeNotFoundError(GameError):
    pass


class InvalidInputError(GameError):
    pass


# 2. Один слот інвентарю
class InventorySlot:
    def __init__(self, item_name: str, quantity: int, max_stack: int):
        self.item_name = item_name  # Назва предмета
        self.quantity = quantity  # Кількість предметів
        self.max_stack = max_stack  # Максимальна кількість у слоті

    def add(self, amount: int) -> int:
        # Додаємо предмети та повертаємо залишок.
        space_left = self.max_stack - self.quantity
        added = min(amount, space_left)
        self.quantity += added
        return amount - added

    def remove(self, amount: int) -> int:
        # Видаляємо предмети зі слоту.
        removed = min(amount, self.quantity)
        self.quantity -= removed
        return amount - removed


# 3. Інвентар гравця
class Inventory:
    def __init__(self, max_slots: int, max_stack: int):
        self.max_slots = max_slots  # Максимальна кількість слотів
        self.max_stack = max_stack  # Максимум предметів у слоті
        self.slots = []  # Список слотів інвентарю

    def add_item(self, item_name: str, quantity: int) -> None:
        # Перевіряємо кількість предметів.
        if quantity <= 0:
            raise InvalidInputError(
                "Кількість предметів має бути більшою за нуль."
            )

        # Рахуємо вільне місце в уже створених слотах.
        space_in_existing = sum(
            self.max_stack - slot.quantity
            for slot in self.slots
            if slot.item_name == item_name
        )

        remaining = max(0, quantity - space_in_existing)

        # Визначаємо, скільки нових слотів потрібно.
        new_slots_needed = (
            remaining + self.max_stack - 1
        ) // self.max_stack

        # Не дозволяємо додати предмети, якщо місця недостатньо.
        if len(self.slots) + new_slots_needed > self.max_slots:
            raise InventoryFullError(
                "Інвентар переповнено! Немає вільних слотів."
            )

        remaining = quantity

        # Спочатку заповнюємо вже наявні слоти.
        for slot in self.slots:
            if slot.item_name == item_name and slot.quantity < self.max_stack:
                remaining = slot.add(remaining)

                if remaining == 0:
                    return

        # Якщо предмети залишилися, створюємо нові слоти.
        while remaining > 0:
            to_add = min(remaining, self.max_stack)

            self.slots.append(
                InventorySlot(item_name, to_add, self.max_stack)
            )

            remaining -= to_add

    def remove_item(self, item_name: str, quantity: int) -> bool:
        # Перевіряємо правильність кількості.
        if quantity <= 0:
            raise InvalidInputError(
                "Кількість для видалення має бути більшою за нуль."
            )

        # Перевіряємо, чи вистачає предметів.
        if self.get_count(item_name) < quantity:
            return False

        remaining = quantity

        # Видаляємо предмети з потрібних слотів.
        for slot in self.slots[:]:
            if slot.item_name == item_name:
                remaining = slot.remove(remaining)

                # Прибираємо порожні слоти.
                if slot.quantity == 0:
                    self.slots.remove(slot)

                if remaining == 0:
                    break

        return True

    def get_count(self, item_name: str) -> int:
        # Підраховуємо загальну кількість предмета.
        return sum(
            slot.quantity
            for slot in self.slots
            if slot.item_name == item_name
        )


# 4. Список інгредієнтів
INGREDIENTS_POOL = [
    "Нічна орхідея", "Срібний папороть", "Вогняний мак",
    "Кровяний мох", "Зоряний пилок", "Корінь мандрагори",
    "Сльози дріади", "Примарна лілія", "Драконів язик",
    "Відьомська мітла", "Болотний ліхтар", "Смолистий бурштин",
    "Морозний бутон", "Золотий трилисник", "Тенева павутина",
    "Пилок феї", "Отруйний плющ", "Пелюстки лотоса",
    "Ігристий бузковий цвіт", "Гірський верес", "Червона крапля",
    "Мертва крапива", "Східний женьшень", "Зоряний чортополох",
    "Білий шип", "Чорний тюльпан", "Огрядний гриб",
    "Сяюча спора", "Плакуча лоза", "Кислотний лист",
    "Громовий корінь", "Пекельний бутон", "Морська губка",
    "Кора ельфійського дуба", "Смола вічнозеленого",
    "Дикий часник", "Північний мох", "Кристалічна трава",
    "Сон-трава", "Озерний очерет", "Зоряний камінь",
    "Сірчаний криста", "Місячний кварц", "Сонячний камінь",
    "Аметистова крихта", "Рубіновий пил", "Смарагдовий уламок",
    "Сапфіровий осколок", "Магнітний залізняк",
    "Обсидіановий шматочок", "Вулканічний попіл", "Морська сіль",
    "Топазова крихта", "Гранатний камінь", "Нефритовий уламок",
    "Флюорит", "Янтарний камінь", "Штучний алмаз",
    "Метеоритний пил", "Залізна окалина", "Мідна руда",
    "Олов'яний злиток", "Срібний пісок", "Золотий змив",
    "Ртутна крапля", "Свинцева кулька", "Кремнієвий камінь",
    "Вапняковий порошок", "Крейдяний біл", "Гранітна крихта",
    "Мармуровий пил", "Слапановий камінь", "Базальтовий осколок",
    "Печерний жемчуг", "Аквамариновий шматочок", "Опаловий блиск",
    "Бірюзова крихта", "Турмаліновий кристал", "Шпінелевий пил",
    "Ціанний камінь", "Луска василіска", "Кіготь грифона",
    "Ікло мантикори", "Шкіра саламандри", "Перо фенікса",
    "Шматочок слизу", "Вусики інсектоїда", "Жало скорпіона",
    "Око жаби", "Кров троля", "Слина химери", "Вовна йєті",
    "Пливкий жир", "Кістка дракона", "Панцир жука",
    "Ріг єдинорога", "Зовнішній хітин", "Серце гарпії",
    "Язик вагіска", "Крило летючої миші", "Плямиста шкура",
    "Мертвий павук", "Вовче ікло", "Ведмежа лапа",
    "Риб'яча луска", "Зміїний отруйний мішок",
    "Жало бджоли-мутанта", "Глазний нерв циклопа",
    "Вухо гобліна", "Кров орка", "Жир морського змія",
    "Півнячий гребінь", "Кіготь гарпії", "Панцир краба",
    "Шкіра хамелеона", "Перо грифона", "Зуб акули",
    "Вуса сома", "Кров вампіра", "Пил привида",
    "Кістка скелета", "Зомбі-плоть", "Мозок мерця",
    "Сльози привида", "Шкіра демона", "Ріг демонічного козла",
    "Крило горгульї", "Павукова залоза", "Кров сирени",
    "Серце русалки", "Кислотна суміш", "Лужний розчин",
    "Алхімічний спирт", "Дистильована вода", "Чистий ефір",
    "Вугільний порошок", "Сірчаний порошок", "Соляна кислота",
    "Селітра", "Нашатирний спирт", "Гліцерин",
    "Оцтова есенція", "Скипидар", "Каніфоль", "Віск",
    "Парафін", "Зола багаття", "Сажа",
    "Длань алхіміка (порошок)", "Есенція сну", "Есенція болю",
    "Рідке золото", "Рідке срібло", "Сяюча рідина",
    "Густий сироп", "В'язка смола", "Сухий лід",
    "Горючий гель", "Мильна піна", "Очищений креозот",
    "Бензинова суміш", "Ароматична олія", "Лавандова олія",
    "М'ятний екстракт", "Хвойний екстракт", "Екстракт алое",
    "Касторове масло", "Льняна олія", "Оливковий жмих",
    "Мигдальна олія", "Пилок комети", "Місячний пил",
    "Сонячний промінь (у склянці)", "Сльоза ангела",
    "Подих дракона", "Пил часу", "Застиглий час",
    "Шматочок туману", "Крапля веселки", "Відгомін бурі",
    "Тінь у пляшці", "Ехо порожнечі", "Зоряне світло",
    "Уламок порталу", "Блискавка в колбі", "Магнітне поле",
    "Радіоактивний мох", "Кристалізований сміх",
    "Сльози розпачу", "Подих зими", "Літній жар",
    "Осінній лист (вічний)", "Весняний бутон (вічний)",
    "Пил з руїн", "Камінь бажань", "Фрагмент долі",
    "Крихта хаосу", "Подих простору", "Золотий вітер",
    "Кришталева тиша"
]


# 5. Список зіль та їхні ціни.
POTIONS_POOL = {
    f"Зілля_сили_{i}": i * 15
    for i in range(1, 51)
}


def generate_recipes():
    # Створюємо рецепти для всіх зіль.
    recipes = {}
    ingredients = iter(INGREDIENTS_POOL)

    for potion in POTIONS_POOL:
        try:
            ingredient1 = next(ingredients)
            ingredient2 = next(ingredients)
        except StopIteration:
            # Якщо інгредієнти закінчилися, вибираємо випадкові.
            ingredient1, ingredient2 = random.sample(INGREDIENTS_POOL, 2)

        # Для рецепта потрібно 2 одиниці першого і 1 другого інгредієнта.
        recipes[potion] = {
            ingredient1: 2,
            ingredient2: 1
        }

    return recipes


RECIPES = generate_recipes()


# 6. Економіка гри
class GameEconomy:
    def __init__(
        self,
        starting_gold=100,
        target_gold=1000,
        max_days=15
    ):
        self.gold = starting_gold  # Початкове золото
        self.target_gold = target_gold  # Ціль для перемоги
        self.max_days = max_days  # Максимальна кількість днів
        self.current_day = 1  # Поточний день

    def sell_potions(
        self,
        potion_name: str,
        quantity: int,
        price_dict: dict
    ) -> int:
        # Розраховуємо ціну проданих зіль.
        price = price_dict.get(potion_name, 10) * quantity
        self.gold += price
        return price

    def check_game_status(self) -> str:
        # Перевіряємо, чи гравець уже переміг.
        if self.gold >= self.target_gold:
            return "win"

        # Перевіряємо, чи закінчилися ігрові дні.
        if self.current_day > self.max_days:
            return "lose"

        return "continue"


# 7. Головна функція гри
def main():
    print("=== АЛХІМІК: RPG ЛАБОРАТОРНА РОБОТА ===")
    print("Мета: заробити 1000 золота за 15 днів, створюючи та продаючи зілля.")
    print("Ліміти: 25 слотів для інгредієнтів і 10 слотів для зілля.")

    # Створюємо інвентарі та економіку гри.
    ingredients_inv = Inventory(max_slots=25, max_stack=25)
    potions_inv = Inventory(max_slots=10, max_stack=10)
    economy = GameEconomy(
        starting_gold=100,
        target_gold=1000,
        max_days=15
    )

    # Видаємо гравцеві початкові інгредієнти.
    try:
        for _ in range(10):
            ingredient = random.choice(INGREDIENTS_POOL)
            ingredients_inv.add_item(ingredient, 5)
    except GameError as error:
        print(f"Не вдалося додати стартові інгредієнти: {error}")

    # Головний цикл гри.
    while True:
        status = economy.check_game_status()

        if status == "win":
            print(f"\n[ПЕРЕМОГА] Ви зібрали {economy.gold} золота!")
            break

        if status == "lose":
            print(
                f"\n[ПОРАЗКА] Час вичерпано. "
                f"Ваш баланс: {economy.gold} золота."
            )
            break

        print(f"\n--- ДЕНЬ {economy.current_day} з {economy.max_days} ---")
        print(f"Золото: {economy.gold}")
        print(f"Слотів зілля: {len(potions_inv.slots)}/10")
        print(f"Слотів інгредієнтів: {len(ingredients_inv.slots)}/25")

        # На початку дня видаємо п'ять випадкових інгредієнтів.
        daily_ingredients = random.choices(INGREDIENTS_POOL, k=5)

        try:
            for ingredient in daily_ingredients:
                ingredients_inv.add_item(ingredient, 1)

            print(
                "Нові інгредієнти: "
                + ", ".join(sorted(set(daily_ingredients)))
            )

        except InventoryFullError:
            print(
                "Інвентар інгредієнтів переповнений. "
                "Не вдалося додати всі бонуси."
            )

        # Меню дій на поточний день.
        while True:
            print("\nМеню:")
            print("1. Переглянути інвентар інгредієнтів")
            print("2. Переглянути рецепти та інвентар зілля")
            print("3. Зварити зілля")
            print("4. Продати зілля та закінчити день")
            print("5. Вийти з гри")

            try:
                choice_text = input("Оберіть дію (1-5): ").strip()

                # Перевіряємо, чи введено число.
                if not choice_text.isdigit():
                    raise InvalidInputError("Введіть число від 1 до 5.")

                choice = int(choice_text)

                if choice not in range(1, 6):
                    raise InvalidInputError("Виберіть варіант від 1 до 5.")

                if choice == 1:
                    # Показуємо всі інгредієнти.
                    print("\n--- Інгредієнти ---")

                    if not ingredients_inv.slots:
                        print("Інвентар інгредієнтів порожній.")
                    else:
                        for slot in ingredients_inv.slots:
                            print(
                                f"{slot.item_name}: "
                                f"{slot.quantity}/{slot.max_stack}"
                            )

                elif choice == 2:
                    # Показуємо перші десять рецептів.
                    print("\n--- Доступні рецепти (перші 10) ---")

                    for potion, requirements in list(RECIPES.items())[:10]:
                        print(
                            f"{potion} | Ціна: {POTIONS_POOL[potion]} золота "
                            f"| Рецепт: {requirements}"
                        )

                    # Показуємо готові зілля в інвентарі.
                    print("\n--- Зілля в інвентарі ---")

                    if not potions_inv.slots:
                        print("Інвентар зілля порожній.")
                    else:
                        for slot in potions_inv.slots:
                            print(
                                f"{slot.item_name}: "
                                f"{slot.quantity}/{slot.max_stack}"
                            )

                elif choice == 3:
                    # Запитуємо назву зілля.
                    potion_name = input(
                        "Введіть точну назву зілля "
                        "(наприклад, Зілля_сили_1): "
                    ).strip()

                    if potion_name not in RECIPES:
                        raise RecipeNotFoundError(
                            "Такого рецепта не існує."
                        )

                    requirements = RECIPES[potion_name]

                    # Перевіряємо наявність усіх інгредієнтів.
                    for ingredient, needed in requirements.items():
                        if ingredients_inv.get_count(ingredient) < needed:
                            raise InsufficientIngredientsError(
                                f"Не вистачає '{ingredient}': "
                                f"потрібно {needed} шт."
                            )

                    # Спочатку додаємо зілля в інвентар.
                    # Якщо місця немає, інгредієнти залишаються у гравця.
                    potions_inv.add_item(potion_name, 1)

                    # Списуємо інгредієнти після успішного додавання зілля.
                    for ingredient, needed in requirements.items():
                        ingredients_inv.remove_item(ingredient, needed)

                    print(f"Зілля {potion_name} успішно зварено!")

                elif choice == 4:
                    # Продаємо всі готові зілля.
                    print("\n--- Продаж зілля ---")
                    earned_today = 0

                    if not potions_inv.slots:
                        print("Немає зіль для продажу.")
                    else:
                        for slot in potions_inv.slots[:]:
                            quantity = slot.quantity

                            earned = economy.sell_potions(
                                slot.item_name,
                                quantity,
                                POTIONS_POOL
                            )

                            earned_today += earned

                            print(
                                f"Продано {quantity} шт. "
                                f"{slot.item_name} за {earned} золота."
                            )

                        # Очищаємо інвентар після продажу.
                        potions_inv.slots.clear()

                        print(
                            f"Загалом зароблено за день: "
                            f"{earned_today} золота."
                        )

                    # Переходимо до наступного дня.
                    economy.current_day += 1
                    break

                elif choice == 5:
                    print("Гру завершено.")
                    return

            # Обробляємо помилки, щоб програма не завершувалася раптово.
            except InvalidInputError as error:
                print(f"[Помилка введення] {error}")

            except InventoryFullError as error:
                print(f"[Помилка інвентарю] {error}")

            except InsufficientIngredientsError as error:
                print(f"[Помилка крафту] {error}")

            except RecipeNotFoundError as error:
                print(f"[Помилка рецепта] {error}")

            except GameError as error:
                print(f"[Помилка гри] {error}")

            except Exception as error:
                print(f"[Непередбачена помилка] {error}")


# Запускаємо гру, якщо цей файл запущено безпосередньо.
if __name__ == "__main__":
    main()