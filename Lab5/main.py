import glob
from PIL import Image
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.model_selection import train_test_split
from torchvision import transforms
from torch.utils.data import DataLoader
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
import random


class Cnn(nn.Module):

    def __init__(self):
        super(Cnn, self).__init__()

        self.layer1 = nn.Sequential(
            nn.Conv2d(3, 16, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(16),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.layer2 = nn.Sequential(
            nn.Conv2d(16, 32, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(32),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.layer3 = nn.Sequential(
            nn.Conv2d(32, 64, kernel_size=3, padding=0, stride=2),
            nn.BatchNorm2d(64),
            nn.ReLU(),
            nn.MaxPool2d(2)
        )

        self.fc1 = nn.Linear(3 * 3 * 64, 10)
        self.dropout = nn.Dropout(0.5)
        self.fc2 = nn.Linear(10, 2)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.layer1(x)
        out = self.layer2(out)
        out = self.layer3(out)
        out = torch.nn.Flatten()(out)
        out = self.relu(self.fc1(out))
        out = self.fc2(out)
        return torch.nn.Sigmoid()(out)


class ADataset(torch.utils.data.Dataset):

    def __init__(self, file_list, transform=None):
        self.file_list = file_list
        self.transform = transform

    # dataset length
    def __len__(self):
        self.filelength = len(self.file_list)
        return self.filelength

    # load an one of images
    def __getitem__(self, idx):
        img_path = self.file_list[idx]
        # print(img_path)
        img = Image.open(img_path)
        img_transformed = self.transform(img.convert("RGB"))  #

        label = img_path.split('/')[-1].split('\\')[0]
        if label == 'cat':
            label = 0
        elif label == 'dog':
            label = 1

        return img_transformed, label


def accuracy(train, val):
    plt.figure(figsize=(15, 5))
    plt.plot(range(len(train)), train, color="green")
    plt.plot(range(len(val)), val, color="red")
    plt.legend(["Train accuracy", "Valid accuracy"])
    plt.show()


def gr_loss(train, val):
    plt.figure(figsize=(15, 5))
    plt.plot(range(len(train)), [float(value) for value in train], color="blue")
    plt.plot(range(len(val)), [float(value) for value in val], color="orange")
    plt.legend(["Train loss", "Valid loss"])
    plt.show()


def creating_train():
    images_list = glob.glob(os.path.join('C:/Users/Admin/Desktop/PythonZachot/lab5/dataset/cat', '*.jpg'))
    images_list2 = glob.glob(os.path.join('C:/Users/Admin/Desktop/PythonZachot/lab5/dataset/dog', '*.jpg'))

    labels = []
    for i in range(len(images_list)):
        labels.append(True)
    for i in range(len(images_list2)):
        labels.append(False)

    for i in images_list2:
        images_list.append(i)

    train_list, train_test_val, train_val, test_val = train_test_split(images_list, labels, test_size=0.2, shuffle=True)
    test_list, val_list, test, val = train_test_split(train_test_val, test_val, test_size=0.5)

    random_idx = np.random.randint(1, len(images_list), size=10)
    fig = plt.figure()
    i = 1
    for idx in random_idx:
        ax = fig.add_subplot(2, 5, i)
        img = Image.open(images_list[idx])
        plt.imshow(img)
        i += 1
        plt.axis('off')
    plt.show()

    func_transforms = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor()
    ])

    train_data = ADataset(train_list, transform=func_transforms)
    test_data = ADataset(test_list, transform=func_transforms)
    val_data = ADataset(val_list, transform=func_transforms)

    train_loader = DataLoader(dataset=train_data, batch_size=10, shuffle=True)
    val_loader = DataLoader(dataset=val_data, batch_size=10, shuffle=True)
    test_loader = DataLoader(dataset=test_data, batch_size=10, shuffle=True)

    device = 'cuda' if torch.cuda.is_available() else 'cpu'

    torch.manual_seed(1234)
    if device == 'cuda':
        torch.cuda.manual_seed_all(1234)

    model = Cnn().to(device)

    optimizer = optim.Adam(params=model.parameters(), lr=0.001)
    criterion = nn.CrossEntropyLoss()

    accuracy_values = []
    loss_values = []
    val_accuracy_values = []
    val_loss_values = []
    model.train()
    epochs = 10
    for epoch in range(epochs):
        epoch_loss = 0
        epoch_accuracy = 0

        for data, label in train_loader:
            data = data.to(device)
            label = label.to(device)

            output = model(data)
            loss = criterion(output, label)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            acc = ((output.argmax(dim=1) == label).float().mean())
            epoch_accuracy += acc / len(train_loader)
            epoch_loss += loss / len(train_loader)
        print('Epoch : {}, train accuracy : {}, train loss : {}'.format(epoch + 1, epoch_accuracy, epoch_loss))
        accuracy_values.append(float(epoch_accuracy))
        loss_values.append(float(epoch_loss))
        model.eval()
        with torch.no_grad():

            epoch_val_accuracy = 0
            epoch_val_loss = 0
            for data, label in val_loader:
                data = data.to(device)
                label = label.to(device)

                val_output = model(data)
                val_loss = criterion(val_output, label)

                acc = ((val_output.argmax(dim=1) == label).float().mean())
                epoch_val_accuracy += acc / len(val_loader)
                epoch_val_loss += val_loss / len(val_loader)

            val_accuracy_values.append(float(epoch_val_accuracy))
            val_loss_values.append(float(epoch_val_loss))
            print('Epoch : {}, val_accuracy : {}, val_loss : {}'.format(epoch + 1, epoch_val_accuracy, epoch_val_loss))
            print('\n')

    accuracy(accuracy_values, val_accuracy_values)
    gr_loss(loss_values, val_loss_values)

    idx = []
    prob = []
    for i in range(len(accuracy_values)):
        idx.append(i)
        prob.append(accuracy_values[i])

    submission = pd.DataFrame({'id': idx, 'label': prob})
    submission.to_csv('result.csv', index=False)


if __name__ == '__main__':
    creating_train()
    id_list = []
    class_ = {1: os.path.join("dataset", "dog"), 0: os.path.join("dataset", "cat")}
    fig = plt.figure()
    while True:
        try:
            i = random.choice(submission['id'].values)
            class_label_random = random.choice(['cat', 'dog'])
            label = submission.loc[submission['id'] == i, 'label'].values[0]
            if label > 0.5:
                label = 1
            else:
                label = 0
            img_path = os.path.join("dataset", f'{class_label_random}.{i:05d}.jpg')
            img = Image.open(img_path)
            plt.imshow(Image.open(img_path))
            plt.axis('off')
            plt.suptitle(class_[label])
            plt.show()
        except Exception as err:
            print(f'error {err}')