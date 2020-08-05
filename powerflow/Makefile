SHELL := /bin/bash

init:
	python3 ./setup/createEnv.py -y
	source powerflow/bin/activate -y && \
	pip install --upgrade pip -y && \
	sudo apt-get install glpk-utils && \
	sudo apt-get install coinor-cbc && \
	pip install -r ./setup/requirements.txt -y
clean:
	rm -R -f powerflow
	rm -R -f __pycache__
	rm -R -f powerflow.egg-info
