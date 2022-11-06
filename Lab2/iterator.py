import os
from next import next_file


class AnnIterator:
    def __init__(self, path: str):
        self.path = path

    def __iter__(self):
        return self

    def __next__(self, direct: str):
        path_new = os.path.join(self.path, direct)
        return next_file(path_new)

if __name__ == "__main__":
    path = "C:/Users/Admin/Desktop/Study/Python/lab 2/dataset_copy"
    Iter = AnnIterator(path)
    print(Iter.__next__('dog_0150.jpg'))
    print(Iter.__next__('dog_0151.jpg'))
    print(Iter.__next__('dog_0152.jpg'))
