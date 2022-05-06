FROM python:3.9

RUN mkdir /app
WORKDIR /app
RUN pip install xmltodict
RUN pip install wget

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
COPY . /app

ENTRYPOINT ["python"]
CMD ["app.py"]

