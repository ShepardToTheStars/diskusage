.PHONY: build test clean

installDependencies:
	@echo "=> Install Missing Dependencies"
	# TODO: virtualenv, make dependency install "smart"
	@echo "TODO"

build: installDependencies
	@echo "=> Build"
	@echo "TODO"

test: installDependencies
	@echo "=> Test"
	python3 test/tests.py

clean:
	@echo "=> Clean"
	rm -rf test/__pycache__
	rm -rf env
	rm -f *.tmp.txt

default: build