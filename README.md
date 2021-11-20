# BD_182_195_249_804
This is the repository for the Big Data Project from PES University about Machine Learning using Spark.

The dataset being streamed has been selected from the google drive which has been provided,

Drive Link - https://drive.google.com/drive/folders/1hKe06r4TYxqQOwEOUrk6i9e15Vt2EZGC

# Streaming Data:

1. Data can be streamed using the stream.py file.
2. To run the streaming file, you will first be required to install the dependencies - numpy, pandas and tqdm. This can be done using pip3.
3. The streaming file takes in 3 arguments with the following flags - --file indicating the dataset to use or the file to be streamed, --batch_size indicating the size of each batch and --endless indicating whether to stream endlessly in a loop. The detailed instructions to run with each flag have been provided as comments inside the script.
4. If you are choosing your own dataset, you will need to write a function to stream your files in this script. Helper functions and instructions have been provided to help you easily add your dataset to the streaming file.
5. The streaming file is well documented and contains comments explaining each code snippet. You are suggested to look at the code and understand the flow. This will help you interface your custom dataset faster.
6. When the streaming begins, you will be able to view the progress of the stream, along with the time taken to completely stream all the data. You are suggested to modify the batch size to ensure that streaming does not take hours to complete.
7. If you are working with a datasetwith a large number of attributes, you may be required to adjust the batch size to a smaller value since there is a limit on how much data can be sent over a TCP connection. If your batch size is larger than what can be sent, the streaming file will display a logging message. The value of the maximum batch size for your dataset can be found out experimentally.


# Processing Stream:

1. The size of each batch will be known to you at runtime. This value will remain constant throughout a single run of the process but can be changed for different experimental runs. It is suggested to hardcode this value inside your process, or recieve it as a command line argument to make implementation of a few functions easier.
2. Data will be streamed using the stream.py file. The batch_size parameter controls the number of examples in each batch. You are suggested to experiment with the batch size and find how the batch size affects performance at each stage of the project – preprocessing, model building and so on.
3. After every batch of data is received, you are required to preprocess them using standard statistical techniques to scale and normalize the values. These include the following (but not limited to):
        -MinMax Scaling
        -Normalization
4. The type of the dataset will determine the type as well as the level preprocessing being performed. For example, if you choose to work with one of the image datasets (such as CIFAR-10) provided, you will have to look into computer vision based techniques such as
        -Convolutions
        -Pooling
        -Masking
        -Greyscale
5. You can either write custom code snippets to perform preprocessing, or use the functions already included as a part of Spark MLlib.
6. Depending on the dataset chosen, you also need to look into the respective feature selection techniques and dimension reduction that Spark MLlib supports to extract features that offer the most importance
      -Compute the variance explained by each feature in your dataset
      -Extract and retain only those features that provide the most variance
7. Depending on the dataset chosen, you may also be required to carry out feature transformation techniques to convert non-numerical data types in numerical data.
8. For each preprocessing step performed, you will be required to explain the reason for carrying it out, as well as provide examples of how it improved performance in the models you build in the later section.
9. Optional: Use plots to show how each preprocessing step makes a difference in the spread nd distribution of your data and compare performance of your models across varying levels of preprocessing performed


# Learning from Data:

1. After each batch has been preprocessed, it needs to be fed into a machine learning model for classification
2. You cannot store all batches in memory. At every instant of time, the model must be re-fit on the input batch such that it learns incrementally, one batch at a time.
3. You must create different classifiers, and fit all of them at the same time on the input batch. You are required to implement atleast 3 classifiers and analyse the performance provided by each. You are further required to use different types of classifiers to understand which type of classifier suits your data the best.
4. Hyperparameter tuning must be performed to obtain the best possible score on your dataset. Which hyperparameters provide maximum changes to your model’s performance? Why? These are questions your experiments must answer. You may even use suitable plots to show how your performance improved with each tuning experiment.
5. Experiment with the training batch size to understand if it plays an important role in predictive modelling. Does increasing the batch size increase performance? Obtain the performance for each of your classifiers on different batch sizes and present them.
6. Optional: Evaluate on the training set and find out how the performance on that training batch varies as the batch size increases. Vary the batch size and obtain the performance of your models on each training batch. Present your performance using suitable plots.


# Testing your Model:

1. Similar to how the input data is streamed, the test data will also be streamed in batches. The size of the input stream may not be the same as that of the training data.
2. For each batch, perform predictions using all the models that you have built.
3. At the end of the stream, compute the performance of each classifier using appropriate metrics such as:
        -Confusion Matrix
        -F-1
        -Accuracy
        -Precision
        -Recall
4. Analyze the difference in the performance between the different types of classifiers (such as linear vs non-linear) and explain the differences. You may use suitable plots to explain the predictions made by your classifiers
5. Make plots of your predictions to compare across different classifiers, hyperparameter choices and batch sizes. While there is no hard limit on the number of plots you create, you are required to create 3 plots per classifier to compare performance and 3 plots showing 3 experiments with the training batch size.
6. Optional: Experiment with the batch size of the test data to understand if the batch size plays a role while making predictions. You will be required to explain your findings, if any
7. Optional: Create random shuffles of the entire dataset to set up cross-validation sets consisting of train and test batches. Evaluate and tune your models on each set of train and test batches and analyse the performance across them.


# Clustering:

1. Similar to the previous sections, your data will be streamed in batches. However, this time the data will be streamed in an endless loop, i.e the first batch will again be streamed after all batches have been streamed.
2. You must fit your clustering algorithm on each batch of input, such that it learns incrementally.
3. Once all batches have been streamed once, compare the centroids obtained in the current iteration with the previous iteration. If the centroids shift by a very small value, stop receiving input from the stream.
4. Set the value of the number of clusters to be the number of classes present in the dataset. Analyse if all the examples in the same class from the test dataset also fall into the same cluster. Answer the question, “Is clustering a form of unsupervised classification?”
5. Optional: Experiment with different batch sizes and different values for the hyperparameters (such as the number of clusters). Do you observe any interesting patterns? Draw conclusions if any.


