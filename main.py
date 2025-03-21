import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Инициализация браузера
browser = webdriver.Firefox()

try:
    # Переход на главную страницу Википедии
    browser.get("https://ru.wikipedia.org/wiki/%D0%97%D0%B0%D0%B3%D0%BB%D0%B0%D0%B2%D0%BD%D0%B0%D1%8F_%D1%81%D1%82%D1%80%D0%B0%D0%BD%D0%B8%D1%86%D0%B0")
    assert "Википедия" in browser.title

    # Запрос у пользователя первоначального поискового запроса
    search_box = browser.find_element(By.ID, "searchInput")
    find_text = input("Введите текст для поиска: ").strip()
    search_box.send_keys(find_text)
    search_box.send_keys(Keys.RETURN)

    # Основной цикл программы
    while True:
        # Печать параграфов текущей статьи
        paragraphs = browser.find_elements(By.TAG_NAME, "p")
        for i, paragraph in enumerate(paragraphs):
            print(f"Параграф {i + 1}: {paragraph.text}")
            input("Нажмите Enter для продолжения...")

        # Предложение пользователю выбора действия
        print("\nВыберите действие:")
        print("1. Листать параграфы текущей статьи")
        print("2. Перейти на одну из связанных страниц")
        print("3. Выйти из программы")
        choice = input("Введите номер действия: ").strip()

        if choice == "1":
            # Продолжаем листать параграфы текущей статьи
            continue

        elif choice == "2":
            # Поиск связанных страниц (внутренних ссылок)
            links = browser.find_elements(By.XPATH, "//div[@class='mw-parser-output']//a[not(contains(@href, 'Category:')) and not(contains(@href, 'File:'))]")
            valid_links = [link for link in links if link.get_attribute("href") and "wiki" in link.get_attribute("href")]

            if not valid_links:
                print("Связанные страницы не найдены.")
                continue

            print("\nДоступные связанные страницы:")
            for i, link in enumerate(valid_links[:10]):  # Показываем только первые 10 ссылок
                print(f"{i + 1}. {link.text}")

            link_choice = input("Введите номер страницы для перехода: ").strip()
            if link_choice.isdigit() and 1 <= int(link_choice) <= len(valid_links):
                selected_link = valid_links[int(link_choice) - 1]
                browser.get(selected_link.get_attribute("href"))
                print(f"Переход на страницу: {selected_link.text}")
            else:
                print("Некорректный выбор. Возвращаемся к текущей странице.")

        elif choice == "3":
            # Выход из программы
            print("Завершение работы программы.")
            break

        else:
            print("Некорректный выбор. Пожалуйста, введите 1, 2 или 3.")

finally:
    # Закрытие браузера
    browser.quit()