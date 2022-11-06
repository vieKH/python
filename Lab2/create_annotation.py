from annotation import Annotation
import os


def create_annotation(path: str, ann: Annotation) -> None:
    """
    :param path: сылки для файла dataset
    :param ann: class Annotation
    :return: ничиго не возращается
    """
    folders = []
    i = 0
    for dirs, folder, files in os.walk(path):

        if i == 0:
            folders = folder
        else:
            for file in files:
                ann.add_line(dirs, file, folders[i-1])
        i += 1


if __name__ == "__main__":
    path_dataset = "C:/Users/Admin/Desktop/Study/Python/pythonProject/dataset"
    Add = Annotation("file_csv.csv")
    create_annotation(path_dataset, Add)
