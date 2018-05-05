#!/usr/bin/env bash


source /etc/bash_completion.d/virtualenvwrapper

git update

# Python 2
mkvirtualenv om --python `which python2`
python setup.py test
python setup.py install
deactivate
rmvirtualenv om

# Python3
mkvirtualenv om --python `which python3`
python setup.py test
python setup.py install
deactivate
rmvirtualenv om
