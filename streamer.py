import sys
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
from pyspark.sql import Row, SparkSession
import json

#Hyper parameters for the dataframe 
WINDOW_DURATION=10
SLIDE_DURATION=2
BATCH_INTERVAL=1

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

...

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


        #This is for debugging , please comment it before continuing
        result=df.collect()
        for i in result:
            print(i[0],i[2])

    except:
        pass

lines.foreachRDD(process)
ssc.start()
ssc.awaitTermination()