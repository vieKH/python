import os
import random
import shutil
from annotation import Annotation


def dataset_random(path: str, path_random: str, ann: Annotation) -> None:
    """
    :param path: Путь к файле dataset
    :param path_random: Путь к новому файле
    :param ann: Класс аннотация
    :return:  не возращается
    """
    if not os.path.isdir(path_random):
        try:
            os.mkdir(path_random)
        except OSError as err:
            print(f"Создать директору {path_random} не успешно")
            raise err

    folders = os.listdir(path)
    for folder in folders:
        files = os.listdir(os.path.join(path, folder))
        for file in files:
            shutil.copy(os.path.join(path, folder, file), path_random)
            file_random = f"{random.randint(1000, 10000)}.jpg"
            while os.path.exists(os.path.join(path_random, file_random)):
                file_random = f"{random.randint(1000, 10000)}.jpg"
            os.rename(os.path.join(path_random, file), os.path.join(path_random, file_random))
            ann.add_line(path_random, file_random, folder)


if __name__ == "__main__":
    path_dataset = "C:/Users/Admin/Desktop/Study/Python/pythonProject/dataset"
    path_task = "C:/Users/Admin/Desktop/Study/Python/lab 2/data_random"
    a = Annotation("file_csv_random.csv")
    dataset_random(path_dataset, path_task, a)
