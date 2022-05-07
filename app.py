from flask import Flask,request,jsonify
import json
import xmltodict
import wget
import sys
import logging
import os

logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)

class DictHolder():
	a = None
	b = None

data = DictHolder()
#holds the data put in from POST app.route() so the GET requests can use it.

holder1 = wget.download("https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA05.xml")
holder2 = wget.download ("https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml")

@app.route('/load',methods = ['POST'])
#load xml files and organize them into searchable dictionaries
def load():
	name1 = holder1 
	#name1 = 'XMLsightingData_citiesUSA05.xml' 
	#The wget fails if running outside of Docker hence direct references but,
	#this is here if the user were to want to run the file outside of Docker.
	name2 = holder2 
	#name2 = 'ISS.OEM_J2K_EPH.xml'
	with open(name1,'r') as f:
		dict1 = json.loads(json.dumps(xmltodict.parse(f.read())))
		dict1modify = dict(enumerate(dict1['visible_passes']['visible_pass']))
		data.a = dict1modify
	with open(name2,'r') as f:
		dict2 = json.loads(json.dumps(xmltodict.parse(f.read())))
		dict2modify = dict(enumerate(dict2['ndm']['oem']['body']['segment']['data']['stateVector']))
		data.b = dict2modify
	logging.debug('POST functional')
	return 'Success!'
		
@app.route('/help',methods = ['GET'])
def help():
	return '\nTo request using this flask app, first call "curl -X POST localhost:5010/load."\n\n Then you can make requests by adding any of the following to the end of \
		" curl localhost:5010 ":\n\n\n/help: #list option for input and what to use \n\n/allEpoch #list all epochs in the positional data\n \n/specEpoch/<epochdate> #lists\
		 all info for a specific epoch\n\n/allCountry/ #lists all countries that exist in the sighting data\n\n/specCountry/<countryname> #list all info on a specific \
		 country \n\n/countryRegions #list all regions associated with specific country\n\n/specRegion #lists all info about a specific region. \n\n/allCities #lists \
		 all cities associated with a specific country AND a specific region \n\n/specCity #lists all info about a specific city from data.\n\n'

@app.route('/allEpoch',methods = ['GET'])
def allepoch():
	results = []
	#print all data related to epochs
	for i in range(len(data.b)):
			k = data.b[i]['EPOCH']
			#print("OUTPUT: " + k)
			results.append(k)
	results = dict(enumerate(results))
	#results is a list object so to return it I turn it into a dict object with dict(enumerate).
	logging.debug('allEpoch functional')
	return	results

@app.route('/specEpoch/<name>',methods = ['GET'])
def specEpoch(name):
	results = []
	# print data relating to a specific epoch
	for i in range(len(data.b)):
			if name == data.b[i]['EPOCH']:
				k=(data.b[i])
				results.append(k)	
	results = dict(enumerate(results))
	logging.debug('specEpoch functional')
	return	results

@app.route('/allCountry', methods = ['GET'])
def allCountry():
	#print all data showing all countries
	results = []
	for i in range(len(data.a)):
			k = (data.a[i]['country'])
			results.append(k)	
	results = dict(enumerate(results))
	logging.debug('allCountry functional')
	return	results

@app.route('/specCountry/<name>',methods = ['GET'])
def specCountry(name):
	results = []
	#print all data relating to a specific country
	for i in range(len(data.a)):
			if name == data.a[i]['country']:
				k = (data.a[i])
				results.append(k)
	results = dict(enumerate(results))
	logging.debug('specCountry functional')
	return	results
@app.route('/countryRegions/<name>',methods = ['GET'])
def countryRegions(name):
	results = []
	#print all regions within a country from data
	for i in range(len(data.a)):
			if name == data.a[i]['country']:
				k = (data.a[i]['region'])
				results.append(k)
	results = dict(enumerate(results))
	logging.debug('countryRegions functional')
	return	results
@app.route('/specRegion/<name>',methods = ['GET'])
def specRegion(name):
	results = []
	#print all data relating to a specific region
	for i in range(len(data.a)):
			if name == data.a[i]['region']:
				k = (data.a[i])
				results.append(k)
	results = dict(enumerate(results))
	logging.debug('specRegion functional')
	return	results
@app.route('/allCities/<name>',methods = ['GET'])
def allCities(name):
	results = []
	#print all cities in a region
	for i in range(len(data.a)):
			if name == data.a[i]['region']:
				k = (data.a[i]['city'])
				results.append(k)
	results = dict(enumerate(results))
	logging.debug('allCities functional')
	return	results

@app.route('/specCity/<name>',methods = ['GET'])
def specCity(name):
	results = []
	#print all data related to a specific city
	for i in range(len(data.a)):
			if name == data.a[i]['city']:
				k = (data.a[i])
				results.append(k)
	logging.debug('specCity functional')
	return	results

if __name__ == '__main__':
	app.run(debug = True, host = '0.0.0.0')
