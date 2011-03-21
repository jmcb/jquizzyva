all:
	python setup.py build
	cp build/lib*/*.pyd util/
