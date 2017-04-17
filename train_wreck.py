import numpy as np
import pandas as pd
#from pyspark import SparkContext,SparkConf
#from pyspark.sql import SQLContext,Row  



#conf=SparkConf().setMaster("master").setAppName("Train_Wreck_Analysis")
#sc = SparkContext(conf=conf)
#sqlContext=SQLContext(sc)


df1=pd.read_csv('/home/mandar/Python_Projects/Train_Wreck/data/train_wreck.csv', na_values=['.'])
#print df1

df2=df1['City, State']
#print df2

city_state_list=[]
states_List=[]

def modifyRow(df2):
	for row in df2:
		if "," in str(row):
			city_state_list.append(str(row))
		else:
			city_state_list.append("N/A,"+str(row))
		
#	print city_state_list
	df4=pd.DataFrame(city_state_list)
	df4=df4.rename(columns={0:'City,State'})
	return df4

def createStatesList(df3):
	for row in df3:
		print row
		if "," in str(row):
			print str(row)
		else:
			continue
		
#	print city_state_list
#	df5=pd.DataFrame(states_List)
#	df5=df5.rename(columns={0:'State'})
#	print df5	


df3=modifyRow(df2)
print df3

#createStatesList(df3)

#cities_dataFrame= df1[df1['City, State'].str.contains(',', na=False)]
#print cities_dataFrame

#df2= np.where(df1['City, State'].str.contains(','));"N/A,"+df1['City, State']
#print df2




