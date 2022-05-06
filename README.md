# ISSdataparser - Parsing Satellite and Ground sighting XML Data with Python

In this file we pull data for ground sighting and satellite location from NASA in an XML format.
## Description
Starting from our folder in isp02, we pull the redis:6 image and install it.
```
docker pull redis:6
```

We start our redis server, making sure to run it in the background using the -d tag/

```
docker run -p 6410:6379 dilipyy-redis redis:6
```
6410:6379 is the connection of our port to the default redis port.
Note that 6410 is my assigned port so yours might be different

To mount a folder to the /data folder that saves 1 bit of  data to the backup every second we call:
```
docker run -d -p 6410:6379 -v $(pwd)/data:/data:rw --name=dilipyy-redis redis:6 --save 1 1
``` 
In the second part of the file, we use flask to interact with the redis server.

To do this, we make sure to import redis in our flask file. We then create a file that reads in data from a json file to a redis server for POST requests, and reads out data from a redis server for GET requests.

To test this, in another terminal section, we open a flask server from our app.py file for the redis server to interact with.

```
Flask run -p 5010
```
Then from the unused terminal we can call commands to either POST or GET from the Flask server which will followup accordingly with the Redis server.

For example
```
curl -x POST localhost:5010/data
```

will result in the Flask object reading in data from ML_Data_Sample.json to the redis server.

Likewise, a GET request,
```
curl localhost:5010
```
will result in the Flask object reading from the redis server and outputting the data in json format. This is accomplished using jsonify.

All of this can then be put into the Dockerfile(the calls for the redis server are within app.py) which then allows the set of files to run separately.

### Dependencies

* Running these files requires: python3, pytest, Flask, GitHub, and Docker and the XML data files linked below.
### Installing
* To install python3 type:
```
brew install python3
```
in the commandline (requires homebrew)
or go to the python website
* To install Flask type:
```
pip3 install --user Flask
```
* To install Docker type:
```
pip3 install --user Docker
```
* To install pytest type:
```
pip3 install --user pytest
```
* ISS position Sampling Data
[ISS.OEM_J2K_EPH.xml](https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml)

* Ground Sighting Sampling Data
[XMLsightingData_citiesUSA05.xml](https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA05.xml)


### Executing program

* To run this file, run the Dockerfile and build the image with:

```
docker build -t <username>,<filename>:version .
```

Then run the docker image with:
```
docker run --name "differentfilename" 5010:5000 <username><filename>:version
```

To see the actual output of the flask server, we will also have to open a second terminal, this is because the flask servers print statements will not show if it is run in the background.

Run the flask server from the docker image
```
flask run -p 5010
```
Then in the other terminal call the flask server with various commands, such as,
```
curl -X POST localhost:5010/load
```
You will then see the output accordingly in the flask server terminal.
