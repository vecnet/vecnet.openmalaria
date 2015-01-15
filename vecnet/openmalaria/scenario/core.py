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
            #attrib = func.__name__
            self.et.find(tag).attrib[attrib] = value
        return inner
    return outer

class Section(object):
    attribs = []
    sections = {}
    def __init__(self, et, schemaVersion=None):
        self.et = et
        self._schemaVersion = schemaVersion

    def __getattr__(self, key):
        """Called when an attribute lookup has not found the attribute in the usual places (i.e. it is not an instance
        attribute nor is it found in the class tree for self). name is the attribute name. This method should return
        the (computed) attribute value or raise an AttributeError exception
        https://docs.python.org/2/reference/datamodel.html#object.__getattr__
        """
        # if key == "sections":
        #     return self.sections

        if key in self.attribs:
            return self.et.attrib[key]
        if key in self.sections:
            # Ignore PyCharm warning below, it got confused by __getattr__ magic
            return self.sections[key](self.et.find(key))
        raise AttributeError()

    # def __setattr__(self, key, value):
    #     if key in self.attribs:
    #         self.et.attrib[key] = value
    #     raise AttributeError()