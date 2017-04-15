from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext,Row  
import numpy as np


conf=(SparkConf().setMaster("local").setAppName("Train_Wreck_Analysis").set("spark.executor.memory","lg"))
sc = SparkContext(conf=conf)
sqlContext=SQLContext(sc)


data_1 = sc.textFile("/home/mandar/Python_Projects/Train_Wreck/data/train_wreck.csv")
#print "------------------------ \nOutput\n\n\nTotal number of rows in spark rdd : "+ str(data.count())  
#print "\n\n\n-------------------------------------------------------"
#print data.top(3)

data_2= data_1.map(lambda x: x.split(","))
print data_2.take(4)

