import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
from pyspark.ml.feature import HashingTF,IDF,Tokenizer
import json

#Hyper parameters for the dataframe 
WINDOW_DURATION=100
SLIDE_DURATION=5
BATCH_INTERVAL=5

def parse_json(x):
    json_obj=json.loads(x)
    inner_json_obj=None
    for key in json_obj.keys():
        inner_json_obj=json_obj[key]
    return(inner_json_obj['feature0'],inner_json_obj['feature1'],inner_json_obj['feature2'])

def getSparkSessionInstance(sparkConf):
    if ("sparkSessionSingletonInstance" not in globals()):
        globals()["sparkSessionSingletonInstance"] = SparkSession \
            .builder \
            .config(conf=sparkConf) \
            .getOrCreate()
    return globals()["sparkSessionSingletonInstance"]

# DataFrame operations inside your streaming program
sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, BATCH_INTERVAL)
lines=ssc.socketTextStream("localhost", 6100).window(WINDOW_DURATION,SLIDE_DURATION)

def process(time, rdd):
    print("========= %s =========" % str(time))
    try:
        # Get the singleton instance of SparkSession
        spark = getSparkSessionInstance(rdd.context.getConf())

        # Convert RDD[String] to RDD[Row] to DataFrame
        rowRdd = rdd.map(parse_json)
        df = spark.createDataFrame(rowRdd)

        df=df.withColumnRenamed("_1","subject").withColumnRenamed("_2","body").withColumnRenamed("_3","classification")

        #df.printSchema()

        #This is for debugging , please comment it before continuing
        """result=df.collect()
        for i in result:
            print(i[0],i[2])"""

        tokenizer=Tokenizer(inputCol="body",outputCol="words")
        wordsData=tokenizer.transform(df)
        
        hashingTF=HashingTF(inputCol="words",outputCol="rawFeatures",numFeatures=20)
        featurizedData=hashingTF.transform(wordsData)

        idf=IDF(inputCol="rawFeatures",outputCol="features")
        idfModel=idf.fit(featurizedData)
        rescaledData=idfModel.transform(featurizedData)

        rescaledData.select("classification","features").show()

        result=rescaledData.collect()
        for i in result:
            print(i["features"])

    except:
        pass

model=None

lines.foreachRDD(process)
ssc.start()
ssc.awaitTermination()