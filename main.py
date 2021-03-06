import os
import sys
import dataProcess
import readData
import CNN_Model
import torch

from FileExe import MainWidget
from PyQt5.QtWidgets import QApplication


if __name__ == '__main__':
    print("Please choose your opreation:\n 1:Training \n 2:Read local picture and predict. \n 3:Exit")
    mode=input("Enter Number:")

    while(not (mode == "1" or mode == "2" or mode == "3" or mode == "dev")):#Get valid input
        print("Please choose your opreation:\n 1:Training \n 2:Read local picture and predict. \n 3:Exit")
        mode = input("Enter Number:")

    if mode=="1":
        print("Now processing raw dataset...")
        dataProcess.convert()
        print("Generating data loaders...")
        train_loader, test_loader1 = readData.generate_loader()
        print("Loading Our Model...")
        model, criterion, optimizer = CNN_Model.giveModel()
        print("Model Loaded")

        print("Training Model...")
        for epoch in range(10):
            CNN_Model.train(epoch, model, criterion, optimizer, train_loader)
            if epoch % 2 == 0:
                if not os.path.exists('./model/'):
                    os.makedirs('./model/')
                torch.save(model, './model/net.pkl')

            CNN_Model.test(torch.load('model/net.pkl'), test_loader1)

    if mode=="2":
        app = QApplication(sys.argv)

        mainWidget = MainWidget()  # A new main widget.
        mainWidget.show()  # Then show this widget.

        exit(app.exec_())

    if mode =="dev":#For developer (Me) only!
        import torch
        from PIL import Image
        import CNN_Model
        from torchvision import transforms

        path = 'test\\157.jpg'
        img = Image.open(path).convert('L')
        resize = transforms.Resize([28, 28])
        testData = resize(img)
        transform = transforms.ToTensor()
        testData = transform(testData)
        model = torch.load('model/net.pkl')
        testData = testData.unsqueeze(0).unsqueeze(0)
        result = CNN_Model.testSingle(model, testData)
        print(result)
    if mode=="3":
        exit()

