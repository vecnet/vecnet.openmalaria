#
# This file is part of the vecnet.openmalaria package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.openmalaria
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.

# This is required to implement namespaces in python 2.x using distutils.
# We have switched to setuptools, so this code is no longer relevant
# http://legacy.python.org/dev/peps/pep-0420/#namespace-packages-today
# Allows other vecnet.* packages (in particular vecnet.emod) to be installed independently
# from pkgutil import extend_path
# __path__ = extend_path(__path__, __name__)

# Note that vecnet is a namespace package.
# Please refer to https://pythonhosted.org/setuptools/setuptools.html#namespace-packages for additional details
#
# This implies that __init__.py in vecnet package MUST contain the line
# __import__('pkg_resources').declare_namespace(__name__)
# This code ensures that the namespace package machinery is operating and the current package is registered
# as a namespace package. You must NOT include any other code and data in a namespace packages's __init__.py

__import__('pkg_resources').declare_namespace(__name__)