import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

browser = webdriver.Firefox()
url = "https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0"
browser.get(url)
assert "Википедия" in browser.title
time.sleep(5)

search_box = browser.find_element(By.ID, "searchInput")
find_text = input("Введите текст для поиска: ")
search_box.send_keys(find_text)
search_box.send_keys(Keys.RETURN)
time.sleep(5)

a = browser.find_element(By.LINK_TEXT, find_text)
a.click()

def menu():
    print("Выберите действие:")
    print("1. Листать параграфы текущей статьи")
    print("2. Перейти на одну из связанных страниц")
    print("3. Выйти из программы")
    try:
        ch = int(input("Введите номер действия: "))
        if ch not in [1, 2, 3]:
            raise ValueError
    except ValueError:
        print("Некорректный выбор. Пожалуйста, введите 1, 2 или 3.")
        return menu()
    return ch

while True:
    choice = menu()
    if choice == 1:
        paragraphs = browser.find_elements(By.TAG_NAME, "p")
        for i, paragraph in enumerate(paragraphs):
            print(f"Параграф {i + 1}: {paragraph.text}")
            choose = input("Нажмите Enter для продолжения... или 0 для выхода в меню: ")
            if input() == "0":
                menu()

    elif choice == 2:
        hatnotes = []
        for element in browser.find_elements(By.TAG_NAME, "div"):
            cl = element.get_attribute("class")
            if cl == "hatnote navigation-not-searchable ts-main":
                hatnotes.append(element)
        for i, note in enumerate(hatnotes):
            name_title = note.find_element(By.TAG_NAME, "a").get_attribute("title")
            print(f"Связанная страница {i + 1}: {name_title}")

        link_choice = int(input("Введите номер страницы для перехода: "))
        hatnote = hatnotes[link_choice - 1]
        link = hatnote.find_element(By.TAG_NAME, "a").get_attribute("href")
        browser.get(link)

    elif choice == 3:
        print("Завершение работы программы.")
        browser.quit()
        break