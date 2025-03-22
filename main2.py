import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Создание браузера
browser = webdriver.Firefox()
url = "https://ru.wikipedia.org/wiki/Заглавная_страница"
browser.get(url)
assert "Википедия" in browser.title
time.sleep(2)  # Небольшая пауза для загрузки страницы

# Функция для поиска информации
def search_wikipedia():
    search_box = browser.find_element(By.ID, "searchInput")
    find_text = input("Введите текст для поиска: ")
    search_box.send_keys(find_text)
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Подождать загрузку результатов
    a = browser.find_element(By.LINK_TEXT, find_text)
    a.click()

# Функция отображения меню
def menu():
    print("\nВыберите действие:")
    print("1. Листать параграфы текущей статьи")
    print("2. Перейти на одну из связанных страниц")
    print("3. Выйти из программы")
    while True:
        try:
            choice = int(input("Введите номер действия: "))
            if choice in [1, 2, 3]:
                return choice
            else:
                print("Некорректный выбор. Введите 1, 2 или 3.")
        except ValueError:
            print("Некорректный ввод. Введите число 1, 2 или 3.")

# Переход по связанным страницам
def navigate_to_related_page():
    hatnotes = []
    for element in browser.find_elements(By.TAG_NAME, "div"):
        cl = element.get_attribute("class")
        if cl == "hatnote navigation-not-searchable ts-main":
            hatnotes.append(element)

    if not hatnotes:
        print("Связанных страниц не найдено.")
        return

    for i, note in enumerate(hatnotes):
        name_title = note.find_element(By.TAG_NAME, "a").get_attribute("title")
        print(f"Связанная страница {i + 1}: {name_title}")

    while True:
        try:
            link_choice = int(input("Введите номер страницы для перехода (или 0 для отмены): "))
            if link_choice == 0:
                return
            elif 1 <= link_choice <= len(hatnotes):
                hatnote = hatnotes[link_choice - 1]
                link = hatnote.find_element(By.TAG_NAME, "a").get_attribute("href")
                browser.get(link)
                time.sleep(3)  # Подождать загрузку новой страницы
                return
            else:
                print("Некорректный выбор. Попробуйте снова.")
        except ValueError:
            print("Некорректный ввод. Введите число.")


# Листание параграфов
def browse_paragraphs():
    paragraphs = browser.find_elements(By.TAG_NAME, "p")
    if not paragraphs:
        print("Параграфы не найдены.")
        return

    for i, paragraph in enumerate(paragraphs):
        print(f"\nПараграф {i + 1}:")
        print(paragraph.text.strip())
        user_input = input("Нажмите Enter для продолжения или 0 для выхода в меню: ")
        if user_input == "0":
            break

# Основной цикл программы
search_wikipedia()

while True:
    choice = menu()
    if choice == 1:
        browse_paragraphs()
    elif choice == 2:
        navigate_to_related_page()
    elif choice == 3:
        print("Завершение работы программы.")
        browser.quit()
        break