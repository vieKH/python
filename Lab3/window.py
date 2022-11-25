import os
from iterator import AnnIterator as AnIt
from annotation import Annotation
from copy_dataset import copy_dataset
from random_dataset import dataset_random
from create_annotation import create_annotation as crt
import sys
from PyQt6.QtWidgets import (QPushButton, QInputDialog, QApplication,
                             QMainWindow, QFileDialog, QLabel)
from PyQt6.QtCore import QSize
from PyQt6 import QtGui


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Work with dataset")
        self.setStyleSheet("background-color : #FFDEAD")
        self.setMinimumSize(800, 400)
        self.dataset_path = QFileDialog.getExistingDirectory(self, 'Выберите папку исходного датасета')


        src = QLabel(f'Исходный датасет:\n{self.dataset_path}', self)
        src.setFixedSize(QSize(250, 50))
        src.move(5, 0)

        button_crt_annotation = self.add_button("Сформировать аннотацию", 250, 50, 5, 50)
        button_crt_annotation.clicked.connect(self.create_annotation)

        button_dataset_copy = self.add_button("Скопировать датасет", 250, 50, 5, 100)
        button_dataset_copy.clicked.connect(self.dataset_copy)

        button_dataset_random = self.add_button("Рандом датасета", 250, 50, 5, 150)
        button_dataset_random.clicked.connect(self.dataset_random)

        path_dog = os.path.join(self.dataset_path, "dog", "0000.jpg")
        iterator_dog = AnIt(path_dog)
        path_cat = os.path.join(self.dataset_path, "cat", "0000.jpg")
        iterator_cat = AnIt(path_cat)

        button_next_dog = self.add_button("Следующая собака", 250, 50, 5, 200)
        button_next_dog.clicked.connect(lambda label="dog", cur_iter=iterator_dog: self.next("dog", cur_iter))

        button_next_cat = self.add_button("Следующий кот", 250, 50, 5, 250)
        button_next_cat.clicked.connect(lambda label="cat", cur_iter=iterator_cat: self.next("cat", cur_iter))

        self.image = QLabel('Нажмите кнопку "Следующая собака" или "Следующий кот".', self)
        self.image.setStyleSheet("color : #800000")
        self.image.resize(400, 300)
        self.image.move(280, 60)

        self.show()

    def add_button(self, name: str, size_x: int, size_y: int, pos_x: int, pos_y: int):
        """Add button with a fixed size and position"""
        button = QPushButton(name, self)
        button.setFixedSize(QSize(size_x, size_y))
        button.move(pos_x, pos_y)
        return button

    def next(self, label: str, cur_iter: AnIt):
        try:
            pixmap = QtGui.QPixmap(cur_iter.__next__())
            self.image.setPixmap(pixmap)
            self.resize(pixmap.size())
            self.adjustSize()
        except StopIteration:
            self.image.setText(f"Изображения {label} закончились.")
        except OSError as err:
            print(err)

    def create_annotation(self) -> None:
        text, ok = QInputDialog.getText(self, 'Ввод',
                                        'Введите название файла-аннотации:')
        if ok:
            a = Annotation(f"{str(text)}.csv")
            crt(self.dataset_path, a)

    def dataset_copy(self):
        path_copy = QFileDialog.getExistingDirectory(self, 'Введите путь к папке')
        if not path_copy:
            return
        text, ok = QInputDialog.getText(self, 'Ввод', 'Введите название файла-аннотации:')
        if ok:
            a = Annotation(f"{str(text)}.cvs")
            copy_dataset(self.dataset_path, path_copy, a)

    def dataset_random(self):
        path_copy = QFileDialog.getExistingDirectory(self, 'Введите путь к папке')
        if not path_copy:
            return
        name, test = QInputDialog.getText(self, 'Ввод', 'Введите название файла-аннотации:')
        if test:
            a = Annotation(f'{str(name)}.csv')
            dataset_random(self.dataset_path, path_copy, a)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()

