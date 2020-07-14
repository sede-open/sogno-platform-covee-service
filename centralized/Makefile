SHELL := /bin/bash

init:
	python3 ./setup/createEnv.py
	source covee/bin/activate && \
	pip install --upgrade pip && \
	sudo apt-get install glpk-utils && \
	sudo apt-get install coinor-cbc && \
	pip install -r ./setup/requirements.txt
clean:
	rm -R -f covee
	rm -R -f __pycache__
	rm -R -f covee.egg-info