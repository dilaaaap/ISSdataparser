NAME ?= dilipyy

all: build

build:    docker build -t dilipyy/issdataparser:latest .

run: docker run --name "ISSdataparser" -d -p 5010:5000 $${NAME}/issdataparser:latest

push:     docker push $${NAME}/issdataparser:latest