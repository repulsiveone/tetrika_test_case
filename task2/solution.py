import csv
import re
from bs4 import BeautifulSoup
import requests
from collections import defaultdict

BASE_URL = 'https://ru.wikipedia.org'

def parse_page(url: str, all_animals: defaultdict):
    """
    Рекурсивно парсит страницы с животными.
    
    Args:
        url (str): URL для парсинга.
        all_animals (defaultdict): Словарь для результатов.
        
    Returns:
        None
    """
    try:
        page = requests.get(url)
        print(f"Статус код:{page.status_code}")

        soup = 	BeautifulSoup(page.text, 'html.parser')
        allAnimals = soup.find_all('div', class_='mw-category mw-category-columns')
        new_url = soup.find('a', string="Следующая страница")
        for data in allAnimals:
            animal_let = data.find('h3').text
            # проверяем чтобы парсились только русские буквы
            if bool(re.search('[а-яА-Я]', animal_let)) is True:
                animal_links = data.find_all('a')
                for _ in animal_links:
                    all_animals[animal_let] += 1
            else:
                return
        # переход на следующую страницу
        if new_url:
            next_url = f"{BASE_URL}/{new_url['href']}"
            parse_page(next_url, all_animals) 
    except requests.RequestException as e:
        print(f"Ошибка при запросе {url}: {e}")

def save_to_csv(data: defaultdict, filename: str):
    """
    Сохраняет данные в CSV файл.
    
    Args:
        data (dict): Данные для сохранения.
    """
    with open(filename, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        for letter, count in data.items():
            writer.writerow([letter, count])

if __name__ == "__main__":
    all_animals = defaultdict(int)
    curr_url = 'https://ru.wikipedia.org/wiki/Категория:Животные_по_алфавиту'
    parse_page(curr_url, all_animals)
    save_to_csv(all_animals, 'beasts.csv')