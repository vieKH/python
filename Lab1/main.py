import logging
import os
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import requests

HEADERS = {"User-Agent": "Mozilla/5.0 Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36",
           "Accept-Language": "en-US, ru-RU", "Accept-Encoding": "grip, deflate", "Connection": "keep-alive", "one": "true"}


def create_file(folder):
    """ Эта фукнция для создании папки
        chdir (change directory) Первый я сделал каталог венрнулся в главный папки
        mkdir (make directory) Создать новую папку (folder)
        Если есть ошибка, она будет появиться на вывод (logging.info)
        :param folder: имена папки """
    try:
        new_directory = os.path.join(folder)
        os.makedirs(new_directory)
    except OSError as err:
        logging.info(f'При создании файл {folder} есть ошибки \n {err}')


def image_write_file(filename, image_url):
    ''' Функция для записи фота в файле
    :param filename: директория файла
    :param image_url: адресс фота
    :return: не возращается
    '''
    picture = requests.get(image_url, HEADERS)
    with open(filename, "wb") as f:
        f.write(picture.content)


def image_download(folder, obj, url, counter=1000):
    """Эта функция для скачать фото
    Из библиотеки request получить код содержать фото
    Мз библиотеки BS4 поменять код в lxml, поиск адресс фото и скачать их
    :param folder: имена папки
    :param obj: объект который вы хотите найти
    :param url: адресс страница ( В задаче https://yandex.ru/images/search?...)
    :param counter: количество фота хотите скачать ( в задаче 1000 фото)
    :return: не возращается значения , для закончить программу когда хватит 1000 фото"""
    create_file(folder)
    arr_image = []
    page = 0
    while counter > 0:
        url = f"{url}?p={page}&text={obj}"
        r = requests.get(url, HEADERS)
        soup = BeautifulSoup(r.text, "lxml")
        images = soup.findAll("img", class_="serp-item__thumb justifier__thumb")
        for image in images:
            if counter == 0:
                return
            image_url = f"https:{image.get('src')}"
            arr_image.append(image_url)
            counter -= 1
        page += 1

    for a in tqdm(range(len(arr_image)), desc=f'Количество фото {folder} уже скачали :'):
        filename = os.path.join(folder, f'{a:04d}.jpg')
        image_write_file(filename, arr_image[a])
    del arr_image


if __name__ == "__main__":
    image_download('dog', 'dog', "https://yandex.ru/images/search")
    image_download('cat', 'cat', "https://yandex.ru/images/search")
