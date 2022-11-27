import os
import csv
import logging


class Annotation:
    def __init__(self, filename: str):
        self.rows = 0
        self.filename = filename
        self.__header = ['Absolute Path', 'Relative Path', 'Label']

    def add_line(self, path: str, filename: str, label: str) -> None:
        with open(self.filename, "a", encoding="utf-8", newline="") as f:
            writer = csv.writer(f, quoting=csv.QUOTE_ALL)
            if self.rows == 0:
                writer.writerow(["Absolute Path", "Relative Path", "Label"])
                self.rows += 1
            writer.writerow([os.path.join(path, filename), os.path.relpath(os.path.join(path, filename)), label])
            self.rows += 1

    def first_file_photo(self, label: str):
        res = []
        try:
            with open(self.filename, 'r') as file:
                rows = csv.DictReader(file)
                if label == "cat":
                    for row in rows:
                        res = [row[self.__header[0]], row[self.__header[1]], row[self.__header[2]]]
                        break
                else:
                    i = 0
                    for row in rows:
                        if i == 1000:
                            res = [row[self.__header[0]], row[self.__header[1]], row[self.__header[2]]]
                            break
                        i += 1
        except OSError as err:
            logging.warning(f' При попытке открытия аннотации {self.filename} произошла ошибка:\n{err}.')
        return res[0]


if __name__ == "__main__":
    path_dataset = "C:/Users/Admin/Desktop/Study/Python/pythonProject/dataset"
    add = Annotation("file_csv.csv")
    print(add.first_file_photo("cat"))
    print(add.first_file_photo("dog"))
    if not os.path.exists("file_csv.csv"):
        print("cvb")
    print(os.path.exists("file_csv.csv"))
