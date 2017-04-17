import numpy as np
import pandas as pd
from pyspark import SparkContext,SparkConf
from pyspark.sql import SQLContext,Row  



conf=SparkConf().setMaster("master").setAppName("Train_Wreck_Analysis")
sc = SparkContext(conf=conf)
sqlContext=SQLContext(sc)


df1=pd.read_csv('/home/mandar/Python_Projects/Train_Wreck/data/train_wreck.csv', na_values=['.'])
#print df1

#df2=pd.DataFrame(df1.)


