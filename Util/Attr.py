# -*- coding: utf-8 -*-
"""Util.Attr - a module providing attribute utility functions """
import collections

def _get_prop(src, name, filt=None):
    """Helper (not exptered) to return the attribute on src named name.
    Callables are called.  A filter is given, then filter(value) is returned
    instead of the value itself.  If something is invalid, None is returned.
    @param src the object being checked for the attribute
    @param name the name of the attribute being checked
    @param filt the optional filter to pass the value through """
    
    if not src or not name:
        return None
    
    val = getattr(src, name, None)
    
    #If val is a function, then call it to get a value
    while val and isinstance(val, collections.Callable):
        val = val()
    
    #If we have a value and a filter, use the filter
    if val and filt:
        val = filt(val)
    
    return val

def get_prop(src, name, filt=None):
    """Helper to return the attribute on src named name.  Callables are
    called. A filter is given, then filter(value) is returned instead of
    the value itself. If something is invalid, None is returned. The
    name is checked with get and '_' prepended and with the first letter
    capitalized.  Suppose the call `get_prop(src, "someProperty")` is
    made.  The following names will be checked IN ORDER:
    
        * someProperty
        * getSomeProperty
        * _someProperty
        * SomeProperty
        * getsomeProperty
        * _SomeProperty
    
    @param src the object being checked for the attribute
    @param name the name of the attribute being checked
    @param filt the optional filter to pass the value through 
    """
    if not src or not name:
        return None
    
    name = name[0].lower() + name[1:]
    pname = name[0].upper() + name[1:]
    
    names = [name, 'get'+pname, '_'+name, pname, 'get'+name, '_'+pname]
    
    for currname in names:
        val = _get_prop(src, currname, filt)
        if val:
            return val
    
    return None
