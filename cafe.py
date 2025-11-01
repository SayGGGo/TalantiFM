# --- Импорты ---
import time
from luckytools import LuckyTools
from datetime import datetime
import json
import tqdm
import requests
from bs4 import BeautifulSoup
import re
import sys
from PIL import Image
import io

WORK_HOUR_START = 7
WORK_HOUR_END = 23

ROLL_CONSTRUCTOR_INGREDIENTS = {
    "wrapper": {
        "Нори": 5,
        "Лосось": 75,
        "Икра": 50,
        "Кунжут": 30,
        "Огурец": 20,
        "Пропустить": 0
    },
    "rice": {
        "Обычный": 20,
        "Солёный": 25
    },
    "filling": {
        "Творожный сыр": 30,
        "Огурецы": 15,
        "Лук": 15,
        "Лосось": 50,
        "Авокадо": 40,
        "Креветка": 80,
        "Угорь": 100,
        "Манго": 50
    }
}

ADULT_MENU_ITEMS = [
    {"name": "Ролл 'Жаркий Чили'", "description": "С угрем, спайси-соусом и перцем халапеньо.", "price_rub": 450.0},
    {"name": "Сет 'Выходной'", "description": "Смелый выбор для ценителей. Много лосося, много огня.",
     "price_rub": 1800.0},
    {"name": "Напиток 'Чай'", "description": "Классический черный чай.", "price_rub": 350.0},
]

# --- LuckyTools инициализация ---
tools = LuckyTools(prefix_short="⌊ Tatsumaki ⌉ »", show_init=False)


# --- Утилиты ---
def get_safe_input(prompt_text, max_val=sys.maxsize, min_val=1):
    while True:
        try:
            answer = input("› ")
            int_answer = int(answer)

            if min_val <= int_answer <= max_val:
                return int_answer

            tools.fade_print(f"✕ Ошибка ввода! Введите число от {min_val} до {max_val}.", white_tag=True, time_show=1.5,
                             color="ff0000")
        except ValueError:
            tools.fade_print("✕ Ошибка ввода! Попробуйте ещё раз.", white_tag=True, time_show=1.5, color="ff0000")


def check_working_hours():
    current_hour = int(str(datetime.now()).split(" ")[1].split(":")[0])
    if WORK_HOUR_START <= current_hour < WORK_HOUR_END:
        return True

    tools.fade_print(f"✕ Мы работаем с {WORK_HOUR_START:02d}:00 до {WORK_HOUR_END:02d}:00", white_tag=True, time_show=3,
                     color="ff0000")
    return False


def get_age_and_name():
    tools.fade_print("Пожалуйста введите своё ФИО:", white_tag=True, time_show=0.01)
    name = input("› ")

    while True:
        try:
            tools.fade_print("Пожалуйста введите свой возраст (только число):", white_tag=True, time_show=0.01)
            age = int(input("› "))
            if 3 < age < 123:
                return age, name
            tools.fade_print("✕ Возраст должен быть в разумных пределах (4-122). Попробуйте ещё раз.", white_tag=True,
                             time_show=3, color="ff0000")
        except ValueError:
            tools.fade_print("✕ Ошибка ввода! Попробуйте ещё раз.", white_tag=True, time_show=3, color="ff0000")


def display_image_from_url(url):
    def pil_to_ascii_color(image):
        BLOCK_CHAR = '\u2588'
        W = 80

        width, height = image.size
        aspect_ratio = height / width
        new_height = int(W * aspect_ratio * 0.55)
        resized_image = image.resize((W, new_height))

        pixels = resized_image.getdata()
        output_string = []

        def get_color_code(r, g, b):
            r_i = int(r / 255 * 5)
            g_i = int(g / 255 * 5)
            b_i = int(b / 255 * 5)
            color_index = 16 + (r_i * 36) + (g_i * 6) + b_i
            return f'\033[38;5;{color_index}m'

        for i, pixel in enumerate(pixels):
            r, g, b = pixel[:3]
            char = BLOCK_CHAR
            color_code = get_color_code(r, g, b)
            output_string.append(f"{color_code}{char}")
            if (i + 1) % W == 0:
                output_string.append('\033[0m\n')

        return "".join(output_string) + '\033[0m'

    try:
        if not url:
            tools.fade_print("| (Нет ссылки на изображение)", white_tag=True, time_show=0.01, color="b5b5b5")
            return

        response = requests.get(url, stream=True, timeout=5)
        response.raise_for_status()

        image = Image.open(io.BytesIO(response.content)).convert("RGB")
        ascii_art = pil_to_ascii_color(image)
        print(ascii_art)

    except requests.exceptions.RequestException:
        tools.fade_print("| Не удалось скачать изображение.", white_tag=True, time_show=0.01, color="ffb300")
    except Exception:
        tools.fade_print("| Ошибка обработки изображения с помощью PIL.", white_tag=True, time_show=0.01,
                         color="ffb300")


# --- Парсинг ---
def pars_ataman():
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/555.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/555.36"
    }
    url = "https://atamansushi.ru/atamansushi/"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.exceptions.RequestException:
        tools.fade_print("✕ Ошибка подключения к сайту", white_tag=True, time_show=3, color="ff0000")
        return []

    soup = BeautifulSoup(response.text, "html.parser")
    rolls_data = []
    current_category = "Неизвестная категория"

    all_relevant_nodes = soup.find_all(
        lambda tag: tag.name == "h2" or (tag.name == "article" and tag.get("itemtype") == "https://schema.org/Product")
    )

    for element in all_relevant_nodes:
        if element.name == "h2":
            current_category = element.text.strip()

        elif element.name == "article" and element.get("itemtype") == "https://schema.org/Product":
            card = element

            name_tag = card.find("img", itemprop="image")
            name = name_tag.get("alt").strip() if name_tag and name_tag.get("alt") else "Без имени"

            weight_tag = card.find("span", class_="product-weight")
            score_tag = card.select_one(".product-score span:not(.icon-container)")
            product_id = card.find("meta", itemprop="productID")
            description = card.find("meta", itemprop="description")
            low_price = card.find("meta", itemprop="lowPrice")
            image_url = card.find("img", itemprop="image")

            price_content = low_price.get("content") if low_price else None
            price = float(price_content) if price_content else 0.0

            rating_text = score_tag.text.strip() if score_tag else None
            try:
                rating = float(rating_text) if rating_text else None
            except ValueError:
                rating = None

            roll = {
                "product_id": product_id.get("content") if product_id else None,
                "name": name,
                "category": current_category,
                "description": description.get("content") if description else "Нет описания",
                "image_url": image_url.get("src") if image_url else None,
                "weight": weight_tag.text.strip() if weight_tag else "Нет веса",
                "price_rub": price,
                "rating": rating
            }

            if roll["name"] != "Без имени" or roll["product_id"]:
                rolls_data.append(roll)

    return rolls_data


def open_constructor(menu, cart, age):
    tools.fade_print("⇌ Конструктор роллов", white_tag=True, time_show=0.01, color="ffffff")
    price = 0
    new_roll_details = {}

    for section_name, ingredients in ROLL_CONSTRUCTOR_INGREDIENTS.items():
        list_ingredients = list(ingredients.items())
        tools.fade_print(f"⇌ Выберите {section_name} (Текущая цена: {price} руб):", white_tag=True, time_show=0.01,
                         color="ffffff")

        for i, (name, cost) in enumerate(list_ingredients):
            tools.fade_print(f"| {i + 1}. {name} - {cost} руб.", white_tag=True, time_show=0.01, color="b5b5b5")

        tools.fade_print(f"| {len(list_ingredients) + 1}. Назад в меню", white_tag=True, time_show=0.01, color="b5b5b5")

        selection_index = get_safe_input("", max_val=len(list_ingredients) + 1)

        if selection_index == len(list_ingredients) + 1:
            return main_menu(menu, cart, age)

        selected_item = list_ingredients[selection_index - 1]
        new_roll_details[section_name] = selected_item
        price += selected_item[1]

    description_text = (
        f"Обертка: {new_roll_details['wrapper'][0]} ({new_roll_details['wrapper'][1]} руб), "
        f"Рис: {new_roll_details['rice'][0]} ({new_roll_details['rice'][1]} руб), "
        f"Начинка: {new_roll_details['filling'][0]} ({new_roll_details['filling'][1]} руб)."
    )

    cart.append({
        "product_id": "0000",
        "name": f"Кастомный ролл ({new_roll_details['wrapper'][0]})",
        "category": "Конструктор роллов",
        "description": description_text,
        "image_url": None,
        "weight": "250 гр",
        "price_rub": float(price),
        "rating": None
    })

    tools.fade_print(f"Итоговая цена: {price} рублей. ✓ Успешно добавлено в корзину.", white_tag=True, time_show=2,
                     color="ffffff")
    main_menu(menu, cart, age)


def open_menu_standart(menu, cart, age):
    print("\n" * 2)
    categories = list(set(item["category"] for item in menu))

    tools.fade_print("⇌ Выберите категорию:", white_tag=True, time_show=0.01, color="ffffff")
    for i, cat in enumerate(categories):
        tools.fade_print(f"| {i + 1}. {cat}", white_tag=True, time_show=0.01, color="b5b5b5")

    tools.fade_print(f"| {len(categories) + 1}. Назад в меню", white_tag=True, time_show=0.01, color="b5b5b5")

    selection_index = get_safe_input("", max_val=len(categories) + 1)
    if selection_index == len(categories) + 1:
        return main_menu(menu, cart, age)

    selected_category = categories[selection_index - 1]

    rolls_in_category = [item for item in menu if item["category"] == selected_category]

    print("\n" * 1)
    tools.fade_print(f"⇌ Выберите блюдо из категории '{selected_category}':", white_tag=True, time_show=0.01,
                     color="ffffff")
    for i, roll in enumerate(rolls_in_category):
        tools.fade_print(f"| {i + 1}. {roll['name']} - {roll['price_rub']} руб.", white_tag=True, time_show=0.01,
                         color="b5b5b5")

    tools.fade_print(f"| {len(rolls_in_category) + 1}. Назад к категориям", white_tag=True, time_show=0.01,
                     color="b5b5b5")

    roll_index = get_safe_input("", max_val=len(rolls_in_category) + 1)
    if roll_index == len(rolls_in_category) + 1:
        return open_menu_standart(menu, cart, age)

    selected_roll = rolls_in_category[roll_index - 1]

    print("\n")
    tools.fade_print(f"Загружаем изображение...", white_tag=True, time_show=0.01, color="ffffff")
    print("\n")
    display_image_from_url(selected_roll['image_url'])

    tools.fade_print(f"⇌ {selected_roll['name']}", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"| Категория: {selected_roll['category']}", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| Описание: {selected_roll['description']}", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| Вес: {selected_roll['weight']}", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| Рейтинг: {selected_roll['rating'] if selected_roll['rating'] else 'Нет'}", white_tag=True,
                     time_show=0.01, color="b5b5b5")
    tools.fade_print(f"|-- Цена: {selected_roll['price_rub']} руб. ------", white_tag=True, time_show=0.01,
                     color="b5b5b5")

    tools.fade_print(f"| 1. Добавить в корзину", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 2. Назад в главное меню", white_tag=True, time_show=0.01, color="b5b5b5")

    action_choice = get_safe_input("", max_val=2)

    if action_choice == 1:
        cart.append(selected_roll)
        tools.fade_print(f"✓ Успешно добавлено в корзину.", white_tag=True, time_show=1.5)
        return main_menu(menu, cart, age)
    else:
        return main_menu(menu, cart, age)


def open_adult_menu(menu, cart, age):
    print("\n" * 2)
    tools.fade_print("!!! ВЗРОСЛОЕ МЕНЮ (18+) !!!", white_tag=True, time_show=0.01, color="ff0000")
    tools.fade_print("⇌ Выберите блюдо:", white_tag=True, time_show=0.01, color="ffffff")

    for i, item in enumerate(ADULT_MENU_ITEMS):
        tools.fade_print(f"| {i + 1}. {item['name']} ({item['description']}) - {item['price_rub']} руб.",
                         white_tag=True, time_show=0.01, color="b5b5b5")

    tools.fade_print(f"| {len(ADULT_MENU_ITEMS) + 1}. Назад в меню", white_tag=True, time_show=0.01, color="b5b5b5")

    roll_index = get_safe_input("", max_val=len(ADULT_MENU_ITEMS) + 1)
    if roll_index == len(ADULT_MENU_ITEMS) + 1:
        return main_menu(menu, cart, age)

    selected_item = ADULT_MENU_ITEMS[roll_index - 1]

    selected_item["product_id"] = f"A{roll_index:03d}"
    selected_item["category"] = "Взрослое меню (18+)"
    selected_item["weight"] = "Различный"
    selected_item["image_url"] = None
    selected_item["rating"] = "5.0"

    cart.append(selected_item)
    tools.fade_print(f"✓ '{selected_item['name']}' успешно добавлено в корзину.", white_tag=True, time_show=2)
    main_menu(menu, cart, age)


def open_menu(menu, cart, age):
    print("\n" * 2)
    tools.fade_print("⇌ Выберите раздел меню:", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print("| 1. Основное меню", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print("| 2. Конструктор роллов", white_tag=True, time_show=0.01, color="b5b5b5")

    option_count = 2
    if age >= 18:
        option_count += 1
        tools.fade_print("| 3. Взрослое меню (18+)", white_tag=True, time_show=0.01, color="ff0000")

    tools.fade_print(f"| {option_count + 1}. Назад в главное меню", white_tag=True, time_show=0.01, color="b5b5b5")

    while True:
        answer = get_safe_input("", max_val=option_count + 1)

        if answer == 1:
            return open_menu_standart(menu, cart, age)
        elif answer == 2:
            return open_constructor(menu, cart, age)
        elif answer == 3 and age >= 18:
            return open_adult_menu(menu, cart, age)
        elif answer == option_count + 1:
            return main_menu(menu, cart, age)
        else:
            tools.fade_print("✕ Некорректный выбор. Попробуйте ещё раз.", white_tag=True, time_show=1.5, color="ff0000")


# --- Корзина и оплата ---
def pay_card(cart, final_price):
    print("\n" * 1)
    tools.fade_print("- Оформление заказа (Карта) -", white_tag=True, time_show=0.01, color="ffffff")

    for item in cart:
        tools.fade_print(f"| {item['name']} - {item['price_rub']} руб", white_tag=True, time_show=0.01, color="b5b5b5")

    tools.fade_print(f"- Итого: {final_price} руб.", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"- Статус: Ожидание оплаты.", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"Для оплаты, переведите {final_price} рублей на номер:", white_tag=True, time_show=0.01,
                     color="b5b5b5")
    tools.fade_print(f"--- +7 923 504 68-72 ---", white_tag=True, time_show=0.01)
    tools.fade_print(f"После перевода, заказ будет принят. Мы свяжемся с вами для уточнения деталей.", white_tag=True,
                     time_show=0.01, color="b5b5b5")


def pay_cash(cart, final_price):
    print("\n" * 1)
    tools.fade_print("- Оформление заказа (Наличными) -", white_tag=True, time_show=0.01, color="ffffff")

    for item in cart:
        tools.fade_print(f"| {item['name']} - {item['price_rub']} руб", white_tag=True, time_show=0.01, color="b5b5b5")

    tools.fade_print(f"- Итого: {final_price} руб.", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"- Статус: Оплата при получении.", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print("Ваш заказ принят. Ожидайте звонка оператора.", white_tag=True, time_show=0.01, color="b5b5b5")


def open_cart(menu, cart, age):
    print("\n" * 2)
    if not cart:
        tools.fade_print("⇌ Корзина пуста.", white_tag=True, time_show=0.01, color="ffffff")
        tools.fade_print("| 1. Назад", white_tag=True, time_show=0.01, color="b5b5b5")
        if get_safe_input("", max_val=1) == 1:
            return main_menu(menu, cart, age)

    final_price = sum(item["price_rub"] for item in cart)

    tools.fade_print("⇌ Ваша Корзина", white_tag=True, time_show=0.01, color="ffffff")
    for i, item in enumerate(cart):
        tools.fade_print(f"| {i + 1}. {item['name']} ({item['category']}) - {item['price_rub']} руб", white_tag=True,
                         time_show=0.01, color="b5b5b5")

    tools.fade_print(f"| --- Итого: {final_price} руб ---------", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"| 1. Оформить заказ", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 2. Назад", white_tag=True, time_show=0.01, color="b5b5b5")

    action_choice = get_safe_input("", max_val=2)

    if action_choice == 2:
        return main_menu(menu, cart, age)

    tools.fade_print("\n⇌ Выберите способ оплаты", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print(f"| 1. Оплата картой", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 2. Наличными при получении", white_tag=True, time_show=0.01, color="b5b5b5")

    payment_choice = get_safe_input("", max_val=2)

    if payment_choice == 1:
        pay_card(cart, final_price)
    elif payment_choice == 2:
        pay_cash(cart, final_price)


# --- Основное меню ---
def main_menu(menu, cart, age):
    print("\n" * 5)
    tools.fade_print("⇌ Главное меню", white_tag=True, time_show=0.01, color="ffffff")
    tools.fade_print("| 1. Меню", white_tag=True, time_show=0.01, color="b5b5b5")
    tools.fade_print(f"| 2. Корзина ({len(cart)})", white_tag=True, time_show=0.01, color="b5b5b5")

    answer = get_safe_input("", max_val=2)

    if answer == 1:
        return open_menu(menu, cart, age)
    elif answer == 2:
        return open_cart(menu, cart, age)


def run_app():
    cart = []

    if not check_working_hours():
        return

    age, name = get_age_and_name()
    tools.fade_print(f"Привет, {name}! Мы рады вас видеть.", white_tag=True, time_show=1)

    menu = []
    try:
        tools.fade_print("Импорт данных меню из JSON...", white_tag=True, time_show=0.01)
        with open("menu.json", "r", encoding="utf-8") as file:
            menu = json.load(file)
        tools.fade_print("✓ Импорт успешно завершён", white_tag=True, time_show=0.01)
    except Exception:
        tools.fade_print("✕ JSON не найден или повреждён. Запуск парсинга сайта...",
                         white_tag=True, time_show=1.5, color="ffb300")
        menu = pars_ataman()
        if menu:
            try:
                with open("menu.json", "w", encoding="utf-8") as file:
                    json.dump(menu, file, indent=4, ensure_ascii=False)
                tools.fade_print("✓ Меню успешно сохранено в menu.json", white_tag=True, time_show=1.5)
            except Exception as e:
                tools.fade_print(f"✕ Ошибка сохранения: {e}", white_tag=True, time_show=3, color="ff0000")
        else:
            tools.fade_print("✕ Не удалось получить данные меню. Выход.", white_tag=True, time_show=3, color="ff0000")
            return

    main_menu(menu, cart, age)


if __name__ == "__main__":
    run_app()
