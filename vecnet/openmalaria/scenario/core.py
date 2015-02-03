# -*- coding: utf-8 -*-
#
# This file is part of the vecnet.openmalaria package.
# For copyright and licensing information about this package, see the
# NOTICE.txt and LICENSE.txt files in its top-level directory; they are
# available at https://github.com/vecnet/vecnet.openmalaria
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License (MPL), version 2.0.  If a copy of the MPL was not distributed
# with this file, You can obtain one at http://mozilla.org/MPL/2.0/.
from xml.etree import ElementTree

def attribute(func):
    """
    Decorator used to declare that property is a tag attribute
    """

    def inner(self):
        name, attribute_type = func(self)
        if not name:
            name = func.__name__
        try:
            return attribute_type(self.et.attrib[name])
        except KeyError:
            raise AttributeError
    return inner


def attribute_setter(attrib_type):
    def outer(func):
        def inner(self, value):
            assert isinstance(value, attrib_type)
            attrib = func.__name__
            self.et.attrib[attrib] = str(value)
        return inner
    return outer


def section(func):
    """
    Decorator used to declare that the property is xml section
    """
    def inner(self):
        return func(self)(self.et.find(func.__name__))
    return inner


def tag_value(func):
    """
    Decorator used to declare that the property is attribute of embedded tag
    """
    def inner(self):
        tag, attrib, attrib_type = func(self)
        return attrib_type(self.et.find(tag).attrib[attrib])
    return inner


def tag_value_setter(tag, attrib):
    """
    Decorator used to declare that the setter function is an attribute of embedded tag
    """
    def outer(func):
        def inner(self, value):
            self.et.find(tag).attrib[attrib] = str(value)
        return inner
    return outer


class Section(object):
    """
    Abstract class, representation of xml section in OpenMalaria input file
    """
    def __init__(self, et):
        self.et = et

    @property
    def xml(self):
        """
        :rtype: str
        """
        return ElementTree.tostring(self.et)
