from flask import Flask, render_template, request, url_for, flash , send_file
from train_wreck import states_visualization
import numpy as np
import pandas as pd
import geocoder
import math
from geopy.geocoders import Nominatim
import bokeh.charts as bc
from bokeh.resources import CDN
from bokeh.embed import components
from bokeh.models import (
  GMapPlot, GMapOptions, ColumnDataSource, Circle, DataRange1d, PanTool, WheelZoomTool, BoxSelectTool
)


app = Flask(__name__)
app.config['DEBUG']=True
app.secret_key = 'super secret key'




df1=pd.read_csv('data/train_wreck.csv', na_values=['.'])
#print df1
df2=df1['City, State']
#print df2
city_state_list=[]
states_List=[]
topTenCitiesList=[]
topTenStates=[]
topTenCitiesCount=[]
city_lat_list=[]
city_long_list=[]

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

city_State_dataFrame=modifyRow(df2)
states_dataFrame=createStatesList(city_State_dataFrame)
states_dataFrame.apply(lambda x: x.astype(str).str.upper())
states_dataFrame['State'] = states_dataFrame['State'].map(lambda x: x.strip())
states_dataFrame['State'] = states_dataFrame['State'].apply(lambda x: x.split(',', 1)[-1])
states_dataFrame['State'] = states_dataFrame['State'].map(lambda x: x.strip())
top_states_dataFrame=states_dataFrame.groupby(['State']).size().reset_index().rename(columns={0:'count'})
all_states_dataFrame=top_states_dataFrame.sort_values(by='count', ascending=False)
top_ten_states_dataFrame=top_states_dataFrame.sort_values(by='count', ascending=False).head(10)


@app.route('/')
def home():
	return render_template('home.html')

@app.route('/visuals/')
def  visuals():
    	
	plot = bc.Bar(data=top_ten_states_dataFrame,values='count',label='State')
	script, div = components(plot)

	error = None
	try:
		return '''
		<!DOCTYPE html>
		<html>
		<head>
			<title>Train Wreck Header</title>
			<meta charset="utf-8">
			<link rel="stylesheet" type="text/css" href="../static/css/bootstrap.min.css">
			<script type="text/javascript" href="../static/js/bootstrap.min.js"></script>
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
			{bokeh_css}
		</head>
		<header style="background-color: #e6e6e6;">
		<!--
			<p> started working </p> -->

			<nav class="navbar navbar-inverse" style="background-color: #4d4d4d;">
				<div class="container-fluid">

					<div class="navbar-header">
						<a class="navbar-brand" href="/" style="color: white;">Train Wreck Analysis</a>
					</div>

					<ul class="nav navbar-nav">
						<li><a href="/">Home</a></li>
						<li><a href="/map/">Map</a></li>
						<li><a href="/visuals/">Bar Chart</a></li>
					</ul>

				</div>
			</nav>
		</header>

		<body>
			<div class="container-fluid" style="margin-left: 20px; float:left; border: solid; border-style: groove; border-width: 5px; height: 650px; width: 700px; padding-top: 20px;">
			 {div}
			 {bokeh_js}
 			 {script}
			</div>
		</body>
		</html>
		'''.format(script=script, div=div, bokeh_css=CDN.render_css(), bokeh_js=CDN.render_js())

	except Exception as e:
		flash(e)
		return render_template('visuals.html', error=error)

@app.route('/map/')
def map():
	scale = 5

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
	#plot.title.text = "Top ten cities"
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
	script, div = components(plot)	




	error = None
	try:
		return '''
		<!DOCTYPE html>
		<html>
		<head>
			<title>Train Wreck Header</title>
			<meta charset="utf-8">
			<link rel="stylesheet" type="text/css" href="../static/css/bootstrap.min.css">
			<script type="text/javascript" href="../static/js/bootstrap.min.js"></script>
			<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.2.1/jquery.min.js"></script>
			{bokeh_css}
		</head>
		<header style="background-color: #e6e6e6;">
		<!--
			<p> started working </p> -->

			<nav class="navbar navbar-inverse" style="background-color: #4d4d4d;">
				<div class="container-fluid">

					<div class="navbar-header">
						<a class="navbar-brand" href="/" style="color: white;">Train Wreck Analysis</a>
					</div>

					<ul class="nav navbar-nav">
						<li><a href="/">Home</a></li>
						<li><a href="/map/">Map</a></li>
						<li><a href="/visuals/">Bar Chart</a></li>
					</ul>

				</div>
			</nav>
		</header>

		<body>
			<div class="container-fluid" style="float:center; border: solid; border-style: groove; border-width: 5px; height: 820px; width: 1200px; padding-top: 2px; padding-left: 42px; padding-right: 2px; margin:0 auto; margin-top: -18px;">
			 {div}
			 {bokeh_js}
 			 {script}
			</div>
		</body>
		</html>
		'''.format(script=script, div=div, bokeh_css=CDN.render_css(), bokeh_js=CDN.render_js())
	except Exception as e:
		flash(e)
		return render_template('map.html',error=error)




if __name__ == '__main__':
	app.run()