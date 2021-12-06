
import sys
from sklearn.base import ClusterMixin
from sklearn.linear_model import Perceptron
import pickle
from pyspark.ml.feature import StandardScaler
import matplotlib.pyplot as plt
from pyspark.ml.feature import CountVectorizerModel
from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from pyspark.mllib.linalg import Vector as MLLibVector, Vectors as MLLibVectors
from pyspark.sql.types import StringType,StructType,StructField
from pyspark import SparkContext
from pyspark import SQLContext
from pyspark.mllib.regression import LabeledPoint
from sklearn.preprocessing import MaxAbsScaler
from sklearn import preprocessing
from sklearn.feature_extraction.text import HashingVectorizer
import numpy as np
from sklearn.metrics import accuracy_score,precision_score
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
from pyspark.ml.feature import HashingTF,IDF,Tokenizer,StringIndexer
from pyspark.ml.feature import RegexTokenizer,StopWordsRemover,CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
from sklearn.metrics.pairwise import pairwise_distances_argmin
from pyspark.mllib.regression import StreamingLinearRegressionWithSGD
from sklearn import linear_model
from pyspark.ml.linalg import Vector
from pyspark.ml.functions import vector_to_array
from sklearn.cluster import MiniBatchKMeans
import json

#Hyper parameters for the dataframe 
"""def parse_json(x):
    json_obj=json.loads(x)
    inner_json_obj=None
    for key in json_obj.keys():
        inner_json_obj=json_obj[key]
    return(inner_json_obj['feature0'],inner_json_obj['feature1'],inner_json_obj['feature2'])"""

def flatten_json(x):
    flattened_json_list=json.loads(x).values()
    for dicts in flattened_json_list:
        for key in dicts:
            dicts[key]=str(dicts[key])
    return(flattened_json_list)


# DataFrame operations inside your streaming program
sc = SparkContext("local[2]", "StreamingMachineLearning")
spark_context=SQLContext(sc)
ssc = StreamingContext(sc, 5)
lines=ssc.socketTextStream("localhost", 6100)

def process(time, rdd):
    #print("========= %s =========" % str(time))
    try:
        if(rdd==[] or rdd is None or rdd==[[]]):
            return
        rdd=rdd.flatMap(lambda x:flatten_json(x))
        df=spark_context.createDataFrame(rdd,["subject","body","label"])

        X=df.select('body').collect()
        X=[row.body for row in X]
        vectorizer=HashingVectorizer(n_features=1000)
        x_train=vectorizer.fit_transform(X)

        scaler=MaxAbsScaler()
        x_train=scaler.fit_transform(x_train)

        y_train=df.select('label').collect()
        y_train=np.array([row[0] for row in np.array(y_train)])

        le = preprocessing.LabelEncoder()
        y_train=le.fit_transform(y_train)

        global count
        global initial_run
        global feature_extraction_pipeline
        """
        (training_data,test_data)=df.randomSplit([0.7,0.3],seed=100)
        feature_extraction_pipeline_fit=feature_extraction_pipeline.fit(training_data)
        feature_extracted_training_data=feature_extraction_pipeline_fit.transform(training_data)
        feature_extracted_testing_data=feature_extraction_pipeline_fit.transform(test_data)

        #feature_extracted_training_data.show(10)
        
        #transformed_df=pipelineFit.transform(test_data)
        #feature_df=transformed_df.select(vector_to_array('features',"float32").alias('features'))
        #print(feature_df.collect())
        #transformed_df.printSchema()

        feature_rdd=feature_extracted_training_data.select('features','indexed_label').rdd
        labels=feature_rdd.map(lambda row: row.indexed_label)
        dense_vector_rdd=feature_rdd.map(lambda row: MLLibVectors.dense(row.features))

        x_train=[]
        for dense_vector in dense_vector_rdd.collect():
            x_train.append(dense_vector.toArray().tolist())
        x_train=np.array(x_train)

        #print("x_train = ",x_train,"\n\n")

        y_train=[]
        for label in labels.collect():
            y_train.append(label)
        y_train=np.array(y_train)

        #print("y_train = ",y_train,"\n\n")

        test_feature_rdd=feature_extracted_testing_data.select('features','indexed_label').rdd
        labels=test_feature_rdd.map(lambda row: row.indexed_label)
        dense_vector_rdd=test_feature_rdd.map(lambda row: MLLibVectors.dense(row.features))

        x_test=[]
        for dense_vector in dense_vector_rdd.collect():
            x_test.append(dense_vector.toArray().tolist())
        x_test=np.array(x_test)

        y_test=[]
        for label in labels.collect():
            y_test.append(label)
        y_test=np.array(y_test)

        #print("y_test = ",y_test,"\n\n")

        clf.partial_fit(x_train,y_train,classes=np.unique(y_train))
        preds=clf.predict(x_test)
        print(preds)

        print("Accuracy Score = ",accuracy_score(y_test,preds))"""
        
        #volabolary=model.stages(2).asInstanceOf[CountVectorizerModel].vocabolary

        """feature_extraction_pipeline_fit=feature_extraction_pipeline.fit(df)
        feature_extracted_training_data=feature_extraction_pipeline_fit.transform(df)

        #vectorizers = [s for s in feature_extraction_pipeline_fit.stages if isinstance(s, CountVectorizerModel)]
        #print([v.vocabulary for v in vectorizers])

        feature_rdd=feature_extracted_training_data.select('features','indexed_label').rdd
        labels=feature_rdd.map(lambda row: row.indexed_label)
        dense_vector_rdd=feature_rdd.map(lambda row: MLLibVectors.dense(row.features))

        x_train=[]
        for dense_vector in dense_vector_rdd.collect():
            x_train.append(dense_vector.toArray().tolist())
        x_train=np.array(x_train)

        y_train=[]
        for label in labels.collect():
            y_train.append(label)
        y_train=np.array(y_train)"""

        clf=None

        if(initial_run):
            initial_run=False
            clf = MiniBatchKMeans()
            #print('Inital run , accuracy cannot be calculated')
        else:
            with open('./mod', 'rb') as p:
                clf = pickle.load(p)
            preds=clf.predict(x_train)
            mbk_means_cluster_centers = np.sort(clf.cluster_centers_, axis = 0)
            mbk_means_labels = pairwise_distances_argmin(x_train, mbk_means_cluster_centers)
            print(count," ",mbk_means_labels)
            count+=1


        clf.partial_fit(x_train)

        pickle.dump(clf, open('./mod', 'wb'))


        #model.trainOn(labeled_point_rdd)
        #model.predictOn(test_feature_rdd).print()

        #targetAndPrediction=transformed_df.select('indexed_label','prediction')
        #predictionAndTargetNumpy=np.array((targetAndPrediction.collect()))
        #print(accuracy_score(predictionAndTargetNumpy[:,0],predictionAndTargetNumpy[:,1]))
    except Exception as e:
        print(str(e))
    
initial_run=True
count=0
stringIndexer=StringIndexer(inputCol='label',outputCol='indexed_label')
model=LogisticRegression(featuresCol='features',labelCol='indexed_label',maxIter=10)
tokenizer=Tokenizer(inputCol="body",outputCol="words")
hashingTf=HashingTF(inputCol=tokenizer.getOutputCol(),outputCol="features1",numFeatures=1000)
scaler=StandardScaler()
scaler.setInputCol('features1')
scaler.setOutputCol('features')
#pickle.dump(clf, open('./mod', 'wb'))

pipeline=Pipeline(stages=[tokenizer,hashingTf,stringIndexer,model])
feature_extraction_pipeline=Pipeline(stages=[tokenizer,hashingTf,scaler,stringIndexer])

lines.foreachRDD(process)


ssc.start()
ssc.awaitTermination()
