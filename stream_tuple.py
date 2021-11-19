from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import json

def parse_json(x):
    json_obj=json.loads(x)
    inner_json_obj=None
    for key in json_obj.keys():
        inner_json_obj=json_obj[key]
    return(inner_json_obj['feature0'],inner_json_obj['feature1'],inner_json_obj['feature2'])

sc = SparkContext("local[2]", "NetworkWordCount")
ssc = StreamingContext(sc, 1)

lines = ssc.socketTextStream("localhost", 6100)
lines=lines.map(parse_json)
lines.pprint()

ssc.start()
ssc.awaitTermination()
