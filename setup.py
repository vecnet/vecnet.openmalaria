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

from setuptools import setup, find_packages

setup(
    name="vecnet.openmalaria",
    version="0.6.0",
    author="Alex Vyushkov, Diggory Hardy",
    author_email="vecnet@vecnet.org",
    description="Openmalaria library for VecNet-CI project",
    license="MPL 2.0",
    keywords="openmalaria malaria vecnet",
    url="https://github.com/vecnet/vecnet.openmalaria",
    # find_packages() takes a source directory and two lists of package name patterns to exclude and include.
    # If omitted, the source directory defaults to the same directory as the setup script.
    packages=find_packages(),  # https://pythonhosted.org/setuptools/setuptools.html#using-find-packages
    namespace_packages=['vecnet', ],
    scripts=['bin/om_expand.cmd', 'bin/om_expand'],
    install_requires=[],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
