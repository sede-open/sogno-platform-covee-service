SHELL := /bin/bash

all:
	$(MAKE) -C centralized init
	$(MAKE) -C powerflow init

clean:
	$(MAKE) -C centralized clean
	$(MAKE) -C powerflow clean
