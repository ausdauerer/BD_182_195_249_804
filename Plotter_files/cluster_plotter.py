import matplotlib.pyplot as plt
import numpy as np

fig, ax = plt.subplots(figsize=(12, 6))
paths=['./outputs/sgdPoints.txt']
#labels=['Passive Aggresive Classifer','Perceptron Classifier','SGD Linear Classifier']
x=[]
y=[]
for index,file in enumerate(paths):
    with open(file) as file:
        lines = file.readlines()
        y_axis = [float(line.rstrip()) for line in lines]
        clusters=np.unique(y_axis)
        dict={}
        for cluster in clusters:
            for i in y_axis:
                if(i==cluster):
                    if(cluster not in dict):
                        dict[cluster]=1
                    else:
                        dict[cluster]+=1
        x.append(dict[0])
        y.append(dict[1])

        X_axis = np.arange(len())

        plt.bar(X_axis - 0.2, Ygirls, 0.4, label = 'Girls')
        plt.bar(X_axis + 0.2, Zboys, 0.4, label = 'Boys')
        plt.ylim([0.8,1.02])
        plt.plot(x_axis,y_axis,label=labels[index])
        plt.xlabel('Batch Number') 
        plt.ylabel('Accuracy') 
        plt.title('SGD Classifier Model (Accuracy vs Batch)') 
        plt.legend(loc="lower right")

plt.show()
