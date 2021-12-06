import matplotlib.pyplot as plt
import sys

fig, ax = plt.subplots(figsize=(12, 6))
paths=['./outputs/sgdPoints.txt','./outputs/sgdPoints100.txt','./outputs/sgdPoints200.txt']
#labels=['Passive Aggresive Classifer','Perceptron Classifier','SGD Linear Classifier']
labels=['Batch Size 50','Batch Size 100','Batch Size 200']
for index,file in enumerate(paths):
    with open(file) as file:
        lines = file.readlines()
        y_axis = [float(line.rstrip()) for line in lines]
        y_axis.insert(0,0)
        x_axis = list(range(0,len(y_axis)))
        plt.ylim([0.8,1.02])
        plt.plot(x_axis,y_axis,label=labels[index])
        plt.xlabel('Batch Number') 
        plt.ylabel('Accuracy') 
        plt.title('SGD Classifier Model (Accuracy vs Batch)') 
        plt.legend(loc="lower right")

plt.show()
