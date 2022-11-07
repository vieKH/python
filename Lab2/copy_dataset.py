from annotation import Annotation
import os
import shutil


def copy_dataset(path: str, path_copy: str, ann: Annotation) -> None:
    """
    :param path: Путь к файле dataset
    :param path_copy: Путь к файле копировании
    :param ann:  класс аннотации
    :return: не возращается
    """
    if not os.path.isdir(path_copy):
        try:
            os.mkdir(path_copy)
        except OSError as err:
            print(f"Создать директору {path_copy} не успешно")
            raise err
    folders = os.listdir(path)
    for folder in folders:
        files = os.listdir(os.path.join(path, folder))
        for file in files:
            shutil.copy(os.path.join(path, folder, file), path_copy)
            os.rename(os.path.join(path_copy, file), os.path.join(path_copy, f"{folder}_{file}"))
            ann.add_line(path_copy, f"{folder}_{file}", folder)


if __name__ == "__main__":
    path_copy = 'C:/Users/Admin/Desktop/Study/Python/lab 2/dataset_copy'
    path = 'C:/Users/Admin/Desktop/Study/Python/pythonProject/dataset'
    a = Annotation("file_csv_copy.csv")
    copy_dataset(path, path_copy, a)
