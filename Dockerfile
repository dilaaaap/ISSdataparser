FROM python:3.9

RUN mkdir /app
WORKDIR /app
RUN pip install xmltodict
RUN pip install wget

RUN wget -P /app/ISS.OEM_J2K_EPH.xml 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml'
RUN wget -P /app/XMLsightingData_citiesUSA05.xml 'https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA05.xml'
RUN pip install Flask==2.0.3
COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]

