#!/usr/bin/env python

import collections

import lxml.etree

import util.load

HEADER = """<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE zyzzyva-search SYSTEM "http://pietdepsi.com/dtd/zyzzyva-search.dtd">
"""

def search_to_type (search):
    for type, inst in util.load.BASE_SEARCH_TYPES.iteritems():
        try:
            if isinstance(search, inst):
                return type
        except TypeError:
            v = search.asdict()
            v.pop("search_type")
            try:
                c = inst(**v)
            except:
                continue
            
            if isinstance(search, inst(**v)):
                return type

    return None

def argument_to_xml_type (argument):
    for key, search_value_type in util.load.SEARCH_VALUES.iteritems():
        if search_value_type.attribute == argument or argument in search_value_type.attribute:
            return key

    return None

def condition_to_type (condition):
    cond = condition.copy()
    cond.pop("search_type", None)

    result = {}

    for ltype, value in cond.iteritems():
        type = argument_to_xml_type(ltype)

        if type is None:
            raise util.load.UnsupportedSearchArgument(ltype)

        result[type] = value

    return result

def condition_to_element (condition):
    el = lxml.etree.Element("condition")
    el.set("type", search_to_type(condition))

    for key, value in condition_to_type(condition.asdict()).iteritems():
        if key == "negated":
            if value is not False:
                value = int(value)
            else:
                continue

        try:
            value = "".join(value) 
        except TypeError:
            pass

        el.set(key, str(value))

    return el

def search_list_to_xml (search_list):
    root = lxml.etree.Element("zyzzyva-search")
    root.set("version", "1")
    conditions = lxml.etree.SubElement(root, "conditions")
    and_set = lxml.etree.SubElement(conditions, "and")
    for search in search_list.searches:
        and_set.append(condition_to_element(search))

    return HEADER + lxml.etree.tostring(root, pretty_print=True)
