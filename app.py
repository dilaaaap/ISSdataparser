from flask import Flask,request,jsonify
import json
import xmltodict
import wget
import sys
app = Flask(__name__)


class DictHolder():
	a = None
	b = None

data = DictHolder()

ep = 'EPOCH'
cou = 'country'
reg  = 'region'
cit = 'city'
holder1 = wget.download("https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA05.xml")
holder2 = wget.download("https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml")

@app.route('/load',methods = ['POST'])
#load xml files and organize them into searchable dictionaries
def load():
	name1 = holder1 #wget.download('https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA05.xml')
	name2 = holder2 #wget.download('https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml')
	with open(name1,'r') as f:
		data1 = xmltodict.parse(f.read())
		json_data1 = json.dumps(data1)
		dict1 = (json.loads(json_data1))
		dict1modify = dict(enumerate(dict1['visible_passes']['visible_pass']))
		data.a = dict1modify
		#print(dict1modify)
		#for key in dict1modify[1]:
		#	print(key)
		#print(json_data1)
	with open(name2,'r') as f:
		data2 = xmltodict.parse(f.read())
		json_data2 = json.dumps(data2)
		dict2 = json.loads(json_data2)
		dict2modify = dict(enumerate(dict2['ndm']['oem']['body']['segment']['data']['stateVector']))
		data.b = dict2modify
		#for key in dict2modify[1]:
		#print(key)
		#print(dict2modify)
		#print(dict2)
		return '\nSuccess! \n'
		
@app.route('/help',methods = ['GET'])
def help():
	return '\nTo request using this flask app, first call "curl -X POST localhost:5010/load."\n\nThen you can make requests by adding any of the following to the end of " curl localhost:5010 ":\n\n\n/help #list option for input and what to use \n\n/allepoch #list all epochs in the positional data\n \n/specEpoch #lists all info for a specific epoch\n\n/allCountry #lists all countries that exist in the sighting data\n\n/specCountry #list all info on a specific country \n\n/countryRegions  #list all regions associated with specific country\n\n/specRegion #lists all info about a specific region	 \n\n/allCities #lists all cities associated with a specific country AND a specific region \n\n/specCity #lists all info about a specific city from data.\n\n'

@app.route('/allepoch',methods = ['GET'])
def allepoch():
	for i in range(len(data.b)):
			print(data.b[i][ep], flush = True)
			yield(data.b[i][ep])
	return 'complete'			
@app.route('/specEpoch/<name>',methods = ['GET'])
def specEpoch(name):
	for i in range(len(data.b)):
			if name == data.b[i][ep]:
				#print
				yield(data.b[i])
	return 'complete'
@app.route('/allCountry', methods = ['GET', ])
def allCountry():
	for i in range(len(data.a)):
			#print
			yield(data.a[i][cou])
	return 'complete'
@app.route('/specCountry/<name>',methods = ['GET'])
def specCountry(name):
	for i in range(len(data.a)):
			if name == data.a[i][cou]:
				#print
				yield(data.a[i])
	return 'complete'
@app.route('/countryRegions/<name>',methods = ['GET'])
def countryRegions(name):
	for i in range(len(data.a)):
			if name == data.a[i][cou]:
				#print
				yield(data.a[i][reg])
	return 'complete'
@app.route('/specRegion/<name>',methods = ['GET'])
def specRegion(name):
	for i in range(len(data.a)):
			if name == data.a[i][reg]:
				#print
				yield(data.a[i])
	return 'complete'	
@app.route('/allCities/<name>',methods = ['GET'])
def allCities(name):
	for i in range(len(data.a)):
			if name == data.a[i][reg]:
				#print
				yield(data.a[i][cit])
	return 'complete'		
@app.route('/specCity/<name>',methods = ['GET'])
def specCity(name):
	for i in range(len(data.a)):
			if name == data.a[i][cit]:
				#print
				yield(data.a[i])
	return 'complete'

#bottom statement
if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0')
