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
#	print df3
	for row in df3['City,State']:
		if "," in str(row):
			states_List.append(str(row).split(",",1)[1])
		
	df5=pd.DataFrame(states_List)
	df5=df5.rename(columns={0:'State'})
	return df5	


city_State_dataFrame=modifyRow(df2)
#print cityState_dataFrame

states_dataFrame=createStatesList(city_State_dataFrame)
#print states_dataFrame

halfComplete_dataFrame= df1[df1['City, State'].str.contains(',', na=False)]
#print halfComplete_dataFrame

cities_dataFrame=pd.DataFrame(halfComplete_dataFrame['City, State'])
cities_dataFrame=cities_dataFrame.rename(columns={'City, State':'City'})
print cities_dataFrame


#df2= np.where(df1['City, State'].str.contains(','));"N/A,"+df1['City, State']
#print df2




