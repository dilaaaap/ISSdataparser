# ISSdataparser - Parsing Satellite and Ground sighting XML Data with Python

In this file we pull data for ground sighting and satellite location from NASA in an XML format.
## Description
NASA has data posted on their website for the ISS satellite as well as data for Ground sightings, of satellites. 
However, this data comes in an xml format, so for us to be able to read through the data to find out more with Python, we will have to make it more usable. In this file we use Docker  to make a containerized Flask app that will convert the xml data into dictionary data that we can iterate over to read specific data that we want out of and that will take GET requests to send the requester data that they want.

## Running program
* To run this file from the Dockerfile on Dockerhub, 
1. download the image from this Dockerhub link:
    [Dockerhub Image File](https://hub.docker.com/repository/docker/dilipyy/issdataparser)
2. Once you have the file downloaded, run the docker image file with
```
docker run --name "ISSdataparser" -d -p 5010:5000 dilipyy/issdataparser:latest
```
This will start the flask server in the background.

3. Then you can call the flask server with various commands, such as,
```
curl -X POST localhost:5000/load
```
for the POST request or
This POST request then initiates the file to pull the xml files from their respective locations using wget, which are then read into the file.

```
    wget.download("https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA05.xml")
    wget.download("https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml")
    
    ...
    @app.route('/load.methods = ['POST'])
    ...
        with open(name1,'r') as f:

    ...
        with open(name2,'r') as f:

```

Because the data is in xml format, it is not very easy to iterate through each of the bits of data, so we must change the structure of the data.

The xmltodict library converts the xml file to a dictionary file, although it does not get rid of the doubled keys everywhere.

``` ...
    data1 = xmltodict.parse(f.read())
    ...
    data2 = xmltodict.parse(f.read())
```
To get rid of these, we process the output of xmltodict further, using json.loads and json.dumps. 

```
    json_data1 = json.dumps(data1)
    dict1 = (json.loads(json_data1))
    ...
    json_data2 = json.dumps(data2)
    dict2 = (json.load(json_data2)
```
    
Following this, we are left with a dictionary full of dictionaries. However, we are not yet able to iterate through this properly. To get to the main chunk of data, we have to remove the outer 'layers' of keys surrounding the data that we want. By inspecting the files, you can achieve this by using dict[key1]...[keyn] to chew through however many layers are necessary to remove headers and other unwanted things. To iterate through this dictionary of dictionaries, we will have to give them each a unique identifier, as keys cannot repeat in the same dictionary. The dict(enumerate()) function does exactly this, and assigns each dictionary a number that we can easily reference to see each individual dictionary. 

```
    dict1modify = dict(enumerate(dict1['visible_passes']['visible_pass']))
    ...
    dict2modify = dict(enumerate(dict2['ndm']['oem']['body']['segment']['data']['stateVector']))
```
Now that we have completed this, we have converted the xml files into datasets that are very compatible with the tools we have in Python, allowing us to complete the GET requests.

4. For examples of GET request input that this can take type:
```
curl localhost:5000/help
```
to get a list of GET request options.
You will then see the output accordingly in the flask server terminal.
* To run this file manually,build the docker image with:
1. 
```
docker build -t dilipyy,issdataparser:latest .
```
2. 
Then run the docker image with:
```
docker run --name "ISSdataparser" -d -p 5010:5000 dilipyy/issdataparser:latest
```
You can then proceed with the step 3 for running the file from the dockerhub file as it is effectively the same from here.

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


