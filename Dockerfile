FROM centos:7.9.2009

RUN yum update -y

RUN yum install -y python3

RUN pip3 install pytest==7.0.0

RUN wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_OEM/ISS.OEM_J2K_EPH.xml /code/ISS.OEM_J2K_EPH.xml

RUN wget https://nasa-public-data.s3.amazonaws.com/iss-coords/2022-02-13/ISS_sightings/XMLsightingData_citiesUSA05.xml /code/XMLsightingData_citiesUSA05.xml

COPY app.py /code/app.py

RUN chmod +rx .code/app.py

ENV PATH "/code:$PATH"


