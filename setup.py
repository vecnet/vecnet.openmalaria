#!/usr/bin/env python
#
# This file is part of the vecnet.openmalaria package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.openmalaria
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
#

from distutils.core import setup

# Utility function to read the README file.
#def read(fname):
#    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name="vecnet.openmalaria",
    version="0.1.0",
    author="Alex Vyushkov, Diggory Hardy",
    author_email="vecnet@vecnet.org",
    description="Bla",
    license="MPLv2",
    keywords="openamalaria",
    url="https://github.com/vecnet/vecnet.openmalaria",
    packages=['vecnet', 'vecnet.openmalaria'],
    #long_description=read('README'),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python",
    ],
)