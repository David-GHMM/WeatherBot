# import re
import requests
from bs4 import BeautifulSoup
from time import sleep

data = {
    'device': 'OS X Chrome v.88.0.4389.90 3a7a0',
    'app_version': '870'
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
}

def find_city(city):
    try:
        sleep(2)
        url = f'https://www.gismeteo.ru/search/{city}/'
        response = requests.get(url, headers=headers, data=data)
    except Exception:
        return False, False

    soup = BeautifulSoup(response.text, 'lxml')

    html_catalog_of_cities = soup.find_all('div', class_="catalog-list")

    try:
        cities_list = html_catalog_of_cities[1]
    except Exception:
        cities_list = html_catalog_of_cities[0]

    possible_city = cities_list.find('a')
    name_city = possible_city.text
    city_url = r'https://www.gismeteo.ru' + possible_city.get('href')

    return name_city, city_url


def get_weather_now(city_url):
    print(city_url)
    try:
        sleep(1.5)
        response = requests.get(city_url + 'now', headers=headers, data=data)
    except Exception:
        return [False]

    soup = BeautifulSoup(response.text, 'lxml')

    try:
        temperature_f = soup.find_all('span', class_='unit unit_temperature_f', limit=2)
        temperature = f"Температура: {int((int(temperature_f[0].text) - 32) * 5 / 9)} °C"
        temperature_by_feeling = f"По ощущениям: {int((int(temperature_f[1].text) - 32) * 5 / 9)} °C"

        wind = f"Ветер: {soup.find('div', class_='unit unit_wind_m_s').text[:1]} м/с"

        humidity = f"Влажность: {soup.find_all('div', class_='item-value', limit=3)[2].text} %"

        time_now = f"Сегодня: {soup.find('div',  class_='now-localdate').text}"

        return [True, time_now, temperature, temperature_by_feeling, wind, humidity]
    except Exception:
        return [False]


def get_weather_today(city_url):
    print(city_url)
    try:
        sleep(1.5)
        response = requests.get(city_url, headers=headers, data=data)
    except Exception:
        return [False]

    soup = BeautifulSoup(response.text, 'lxml')

    # try:
    temperature_f = soup.find_all('span', class_='unit unit_temperature_c', limit=4)
    temperature_min = f"Мин. температура: {temperature_f[2].text} °C"
    temperature_max = f"Макс. температура: {temperature_f[3].text} °C"

    windy = [int(i.text) for i in soup.find_all('span', class_='wind-unit unit unit_wind_m_s')]
    wind = f'Ветер: от {min(windy[8:])} до {max(windy[8:])} м/с'

    humidityy = [int(i.text) for i in soup.find_all('div', class_='row-item', limit=97)[88:96]]
    humidity = f"Средняя влажность: {sum(humidityy)//8} %"

    date = f"Сегодня: {soup.find('div', class_='date date-7').text}"

    return [True, date, temperature_max, temperature_min, wind, humidity]
    # except Exception:
    #     print('asdsa')
    #     return [False]


def get_weather_tomorrow(city_url):
    print(city_url)
    try:
        sleep(1.5)
        response = requests.get(city_url + 'tomorrow', headers=headers, data=data)
    except Exception:
        return [False]

    soup = BeautifulSoup(response.text, 'lxml')


def get_weather_3rd_day(city_url):
    print(city_url)
    try:
        sleep(1.5)
        response = requests.get(city_url + '3-day', headers=headers, data=data)
    except Exception:
        return [False]

    soup = BeautifulSoup(response.text, 'lxml')


def get_weather_other_day(city_url):
    print(city_url)
    try:
        sleep(1.5)
        response = requests.get(city_url + 'now', headers=headers, data=data)
    except Exception:
        return [False]

    soup = BeautifulSoup(response.text, 'lxml')
