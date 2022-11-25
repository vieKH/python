import os
from next import next_file


class AnnIterator:
    def __init__(self, path: str):
        self.path = path

    def __iter__(self):
        return self

    def __next__(self):
        if self.path == next_file(self.path):
            raise StopIteration
        self.path = next_file(self.path)
        return self.path


if __name__ == "__main__":
    path = "C:/Users/Admin/Desktop/Study/Python/pythonProject/dataset/dog"
    path_new = os.path.join(path, "0001.jpg")
    Iter = AnnIterator(path_new)
    print(Iter.__next__())
    print(Iter.__next__())
    print(Iter.__next__())

