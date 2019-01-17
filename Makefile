.PHONY: demo1 demo2 centos build test clean

demo1:
	python3 diskusage.py -i 2 /private/var/vm
	@echo "\n________________________________________________\n"
	ls -l /private/var/vm

demo2
	rm -f demo2.tmp.json
	python3 diskusage.py --debug -i 2 / > demo2.tmp.json
	tail -n 1000 demo2.tmp.json

build:
	@echo "=> Build"
	@echo "TODO"

test: 
	@echo "=> Test"
	python3 test/tests.py

clean:
	@echo "=> Clean"
	rm -rf test/__pycache__
	rm -rf env
	rm -f *.tmp.txt

default: build