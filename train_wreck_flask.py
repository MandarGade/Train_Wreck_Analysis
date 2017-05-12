from flask import Flask, render_template, request, url_for, flash , send_file
from train_wreck import states_visualization

app = Flask(__name__)
app.config['DEBUG']=True
app.secret_key = 'super secret key'



@app.route('/')
def home():
	return render_template('home.html')

@app.route('/map/',methods=["GET"])
def  map():
#	return render_template('map.html')
	error = None
	try:
		if request.method == "GET":
			print "Request received at the map server....."
			return render_template('map.html')
	except Exception as e:
		flash(e)
		return render_template('map.html',error=error)

@app.route('/visuals/', methods=["GET"])
def bar():

	error = None
	try:
		if request.method == "GET":
			print "Request received at the visuals server....."
			states,count,all_states,all_states_count = states_visualization()

			print states
			print count
			print "------------------------------------"
			print all_states
			print all_states_count
			return render_template('visuals.html')
	except Exception as e:
		flash(e)
		return render_template('visuals.html',error=error)




if __name__ == '__main__':
	app.run()