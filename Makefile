NAME ?= dilipyy

all: 
	build run push

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker build -t ${NAME}/issdataparser:1.0 .

run:
	docker run --rm -v \${PWD}:/data ${NAME}/issdataparser:1.0  ISSdataparser.py

push: 
	docker push ${NAME}/issdataparser.py:1.0
