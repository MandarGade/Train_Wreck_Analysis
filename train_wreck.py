import numpy as np
import pandas as pd
import geocoder
import math
import folium
#import gmplot

import matplotlib.pyplot as plt
#from mpl_toolkits.basemap import Basemap
from geopy.geocoders import Nominatim
from matplotlib.patches import Polygon


import bokeh.charts as bc
from bokeh.plotting import output_file,show
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)


df1=pd.read_csv('data/train_wreck.csv', na_values=['.'])
#print df1

df2=df1['City, State']
#print df2
#
city_state_list=[]
states_List=[]
topTenCitiesList=[]
topTenStates=[]
topTenCitiesCount=[]
city_lat_list=[]
city_long_list=[]

#---------------------------------------------------------------------------------------------------------------------------------


def modifyRow(df2):
	for row in df2:
		if "," in str(row):
			city_state_list.append(str(row))
		else:
			city_state_list.append("N/A,"+str(row))

	df4=pd.DataFrame(city_state_list)
	df4=df4.rename(columns={0:'City,State'})
	return df4

#---------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------
def createStatesList(df3):	
	for row in df3['City,State']:
		if "," in str(row):
			states_List.append(str(row).split(",",1)[1])
		
	df5=pd.DataFrame(states_List)
	df5=df5.rename(columns={0:'State'})
	return df5	

#---------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------

def cities_visualization():
	scale = 5
	lat_tpl=()
	long_tpl=()
	cities_tpl=()
	'''
		create a dataframe without null row or column values 
	'''
	halfComplete_dataFrame= df1[df1['City, State'].str.contains(',', na=False)]

	cities_dataFrame=pd.DataFrame(halfComplete_dataFrame['City, State'])
	cities_dataFrame=cities_dataFrame.rename(columns={'City, State':'City'})
	top_cities_dataFrame=cities_dataFrame.groupby(['City']).size().reset_index().rename(columns={0:'count'})
	top_ten_cities_dataFrame=top_cities_dataFrame.sort_values(by='count', ascending=False).head(10)

	geolocator = Nominatim()


	lat_long_list=[]
	for row in top_ten_cities_dataFrame['City']:
		topTenCitiesList.append(str(row))
	#print topTenCitiesList

	
	for row in top_ten_cities_dataFrame['count']:
    		topTenCitiesCount.append(row)
    	
		
	#print topTenCitiesCount
	
	for i,val in enumerate(topTenCitiesList):
		loc=geolocator.geocode(val)
		#cities_tpl=cities_tpl+(val,)
		#long_tpl=long_tpl+(loc.longitude,)
		#lat_tpl=lat_tpl+(loc.latitude,)
		city_lat_list.append(loc.latitude)
		city_long_list.append(loc.longitude)

	#print topTenCitiesList
	#print topTenCitiesCount
	#print city_lat_list
	#print city_long_list
	#print cities_tpl
	map_options = GMapOptions(lat=39.8282, lng=-98.5795, map_type="roadmap", zoom=5)
	plot = GMapPlot(
    x_range=DataRange1d(), y_range=DataRange1d(), map_options=map_options, plot_width=1100, plot_height=800)
	plot.title.text = "Top ten cities"
	plot.api_key = "AIzaSyBfcQ8lTsXC5du_Mj0IyFLuXepDt_Euawo"
	source = ColumnDataSource(
    data=dict(
        lat=city_lat_list,
        lon=city_long_list,
		#text=topTenCitiesList,
    ))
	circle = Circle(x="lon", y="lat", tags=topTenCitiesList, size=15, fill_color="blue", fill_alpha=0.8, line_color=None)
	plot.add_glyph(source, circle)
	plot.add_tools(PanTool(), WheelZoomTool(), BoxSelectTool())
	output_file("gmap_plot.html")
	show(plot)



#---------------------------------------------------------------------------------------------------------------------------------




#---------------------------------------------------------------------------------------------------------------------------------

def states_visualization():
	'''
		create a dataframe for city and states values
	'''
	city_State_dataFrame=modifyRow(df2)
	'''
		finding top ten states with most accidents
	'''
	states_dataFrame=createStatesList(city_State_dataFrame)
	states_dataFrame.apply(lambda x: x.astype(str).str.upper())
	states_dataFrame['State'] = states_dataFrame['State'].map(lambda x: x.strip())
	#states_dataFrame['States'].str.split(',').str.get(1)
	states_dataFrame['State'] = states_dataFrame['State'].apply(lambda x: x.split(',', 1)[-1])
	states_dataFrame['State'] = states_dataFrame['State'].map(lambda x: x.strip())
	#print states_dataFrame
	top_states_dataFrame=states_dataFrame.groupby(['State']).size().reset_index().rename(columns={0:'count'})
	#print top_states_dataFrame
	all_states_dataFrame=top_states_dataFrame.sort_values(by='count', ascending=False)
#	print all_states_dataFrame
	all_states=[]
	all_states_count=[]
	#all_states_tpl=()
	for a, b in all_states_dataFrame.itertuples(index=False):
	    	all_states.append(a)
	    	all_states_count.append(b)
	    	#all_states_tpl=all_states_tpl+(a,)
	#all_states=zip(all_states,all_states_count)
	#all_states=dict(all_states)
	#print all_states

	top_ten_states_dataFrame=top_states_dataFrame.sort_values(by='count', ascending=False).head(10)
	print top_ten_states_dataFrame
	#states={}
	state=[]
	count=[]
	states_tpl=()
	for a, b in top_ten_states_dataFrame.itertuples(index=False):
	    	state.append(a)
	    	count.append(b)
	    	#states_tpl=states_tpl+(a,)
	#states=zip(state,count)
	#states=dict(states)
	
	#print states
	output_file('bar_graph.html')
	plot = bc.Bar(data=top_ten_states_dataFrame,count='count',label='State')
	show(plot)

	bc.Bar


'''	
	y_pos = np.arange(len(states_tpl))
	performance = count
	plt.figure(figsize=(15,12))
	plt.bar(y_pos, performance, align='center', alpha=0.6)
	plt.xticks(y_pos, states_tpl)
	plt.ylabel('Number of Accidents')
	plt.title('Top ten states for train accidents')
#	plt.savefig('static/images/barchart.png')
	plt.show()

 '''
	
#	return state,count,all_states,all_states_count





if __name__ == '__main__':
	cities_visualization()
#	states_visualization()
