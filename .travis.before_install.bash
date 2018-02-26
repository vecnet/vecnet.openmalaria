#!/usr/bin/env bash

if [ "$TRAVIS_OS_NAME" == "linux" ]; then
	echo "OK"
elif [ "$TRAVIS_OS_NAME" == "osx" ]; then
	pip install virtualenv
	virtualenv -p $PYTHON /tmp/venv
	source /tmp/venv/bin/activate
	pip install -U pytest
fi

pip install coverage
pip install pytest-cov
pip install coveralls