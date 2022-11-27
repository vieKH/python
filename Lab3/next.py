import os
import re


def next_file(path: str):
    """
    :param path: Путь к папки
    :return: Следующий экземпляр класса или None
    """
    if not os.path.exists(path):
        raise FileExistsError(f'Файл по {path} не существует')
    direct, filename = os.path.split(path)
    a = "".join(re.findall(r'\d', filename))
    number = int(a) + 1
    file_new = re.sub(a, f'{number:04d}', filename)
    file_new = os.path.join(direct, file_new)
    if os.path.exists(file_new):
        return file_new
    else:
        raise FileExistsError(f'Файл по пути {file_new} не существует.')
