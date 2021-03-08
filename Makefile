SHELL := /bin/bash

all:
	$(MAKE) -C covee init
	$(MAKE) -C covee-powerflow init

clean:
	$(MAKE) -C covee clean
	$(MAKE) -C covee-powerflow clean

ext:
	python3.6 ./setup_ext/createEnv.py -y 
	source venv_ext/bin/activate -y && \
	sudo apt-get install python3-venv && \
	pip install --upgrade pip && \
	pip install -r ./setup_ext/requirements.txt 

clean_ext:
	rm -R -f venv_ext
	rm -R -f __pycache__
	rm -R -f venv_ext.egg-info
