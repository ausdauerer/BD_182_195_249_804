
"""This program applies non-incremental logistic regression for classification a
and prints the accuracy for each batch"""


import sys
from pyspark.sql.types import StringType,StructType,StructField
from pyspark import SparkContext
from pyspark import SQLContext
import numpy as np
from sklearn.metrics import accuracy_score,precision_score
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
from pyspark.ml.feature import HashingTF,IDF,Tokenizer,StringIndexer
from pyspark.ml.feature import RegexTokenizer,StopWordsRemover,CountVectorizer
from pyspark.ml.classification import LogisticRegression
from pyspark.ml import Pipeline
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
    print("========= %s =========" % str(time))
    try:
        if(rdd==[] or rdd is None or rdd==[[]]):
            return
        rdd=rdd.flatMap(lambda x:flatten_json(x))
        df=spark_context.createDataFrame(rdd,["subject","body","label"])
        #df.show(10)

        (training_data,test_data)=df.randomSplit([0.7,0.3],seed=100)
        pipelineFit=pipeline.fit(training_data)
        #fea_df=model.transform(df)
        #fea_df.show(10)
        targetAndPrediction=pipelineFit.transform(test_data).select('indexed_label','prediction')
        predictionAndTargetNumpy=np.array((targetAndPrediction.collect()))
        print(accuracy_score(predictionAndTargetNumpy[:,0],predictionAndTargetNumpy[:,1]))
    except:
        print("No Data")
    
stringIndexer=StringIndexer(inputCol='label',outputCol='indexed_label')
model=LogisticRegression(featuresCol='features',labelCol='indexed_label',maxIter=10)
tokenizer=Tokenizer(inputCol="subject",outputCol="words")
hashingTf=HashingTF(inputCol=tokenizer.getOutputCol(),outputCol="features")

pipeline=Pipeline(stages=[tokenizer,hashingTf,stringIndexer,model])
lines.foreachRDD(process)
ssc.start()
ssc.awaitTermination()