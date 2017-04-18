import numpy as np
import pandas as pd
import geocoder
import math
#import gmplot

import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from matplotlib.patches import Polygon

#from pyspark import SparkContext,SparkConf
#from pyspark.sql import SQLContext,Row  



#conf=SparkConf().setMaster("master").setAppName("Train_Wreck_Analysis")
#sc = SparkContext(conf=conf)
#sqlContext=SQLContext(sc)


df1=pd.read_csv('/home/mandar/Python_Projects/Train_Wreck/data/train_wreck.csv', na_values=['.'])
#print df1

df2=df1['City, State']
#print df2
#
city_state_list=[]
states_List=[]
topTenCitiesList=[]
topTenStates=[]


def modifyRow(df2):
	for row in df2:
		if "," in str(row):
			city_state_list.append(str(row))
		else:
			city_state_list.append("N/A,"+str(row))

	df4=pd.DataFrame(city_state_list)
	df4=df4.rename(columns={0:'City,State'})
	return df4

def createStatesList(df3):	
	for row in df3['City,State']:
		if "," in str(row):
			states_List.append(str(row).split(",",1)[1])
		
	df5=pd.DataFrame(states_List)
	df5=df5.rename(columns={0:'State'})
	return df5	

def cities_visualization(df):
	scale = 5

	map = Basemap(llcrnrlon=-119,llcrnrlat=22,urcrnrlon=-64,urcrnrlat=49,
        projection='lcc',lat_1=32,lat_2=45,lon_0=-95)

	map.readshapefile('st99_d00', name='states', drawbounds=True)

	geolocator = Nominatim()


	lat_long_list=[]
	for row in df['City']:
		topTenCitiesList.append(str(row))
	#print topTenCitiesList

	for i,val in enumerate(topTenCitiesList):
		#print val
		lat_long_list.append(geocoder.google(val).latlng)
		#print lat_long_list[i]
		#loc=geolocator.geocode(val)
		#x, y = map(loc.longitude, loc.latitude)
		#print str(x)+" , "+str(y)
    	#map.plot(x,y,marker='o',color='Red',markersize=5)
	#plt.show()








def states_visualization(df):
	for row in df['State']:
		topTenStates.append(row)
	print topTenStates






city_State_dataFrame=modifyRow(df2)
#print cityState_dataFrame

#
#
# Findind top ten states with most accidents
#
#
states_dataFrame=createStatesList(city_State_dataFrame)
#print states_dataFrame
top_states_dataFrame=states_dataFrame.groupby(['State']).size().reset_index().rename(columns={0:'count'})
top_ten_states_dataFrame=top_states_dataFrame.sort_values(by='count', ascending=False).head(10)
#print top_ten_states_dataFrame


#
#
# Creating a dataframe which has all rows information
#
#
halfComplete_dataFrame= df1[df1['City, State'].str.contains(',', na=False)]
#print halfComplete_dataFrame


#
#
# Findind top ten cities with most accidents
#
#
cities_dataFrame=pd.DataFrame(halfComplete_dataFrame['City, State'])
cities_dataFrame=cities_dataFrame.rename(columns={'City, State':'City'})
top_cities_dataFrame=cities_dataFrame.groupby(['City']).size().reset_index().rename(columns={0:'count'})
top_ten_cities_dataFrame=top_cities_dataFrame.sort_values(by='count', ascending=False).head(10)





#
#
# Calling Visualization Methods
#
#
#cities_visualization(top_ten_cities_dataFrame)
states_visualization(top_ten_states_dataFrame)


