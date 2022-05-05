NAME ?= dilipyy

all: build run push

images:
	docker images | grep ${NAME}

ps:
	docker ps -a | grep ${NAME}

build:
	docker build -t $(NAME)/ml_data_analysis:1.0 .

run:
	docker run --rm -v \${PWD}:/data ${NAME}/ml_data_analysis:1.0 ml_data_analaysis.py /data/Meteorite_Landings.json

push: docker push ${NAME}/ml_data_analysis:1.0
