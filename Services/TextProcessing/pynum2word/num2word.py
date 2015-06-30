'''
Module: num2word.py
Requires: num2word_*.py
Version: 0.2

Author:
   Taro Ogawa (tso@users.sourceforge.org)
   
Copyright:
    Copyright (c) 2003, Taro Ogawa.  All Rights Reserved.

Licence:
    This module is distributed under the Lesser General Public Licence.
    http://www.opensource.org/licenses/lgpl-license.php

Usage:
    from num2word import to_card, to_ord, to_ordnum
    to_card(1234567890)
    to_ord(1234567890)
    to_ordnum(12)

Notes:
    The module is a wrapper for language-specific modules.  It imports the
    appropriate modules as defined by locale settings.  If unable to
    load an appropriate module, an ImportError is raised.

History:
    0.2: n2w, to_card, to_ord, to_ordnum now imported correctly
'''
import locale as _locale

# Correct omissions in locale:
# Bugrep these...
_locdict = { "English_Australia" : "en_AU", }


_modules = []
for _loc in [_locale.getlocale(), _locale.getdefaultlocale()]:
    _lang = _loc[0]
    if _lang:
        _lang = _locdict.get(_lang, _lang)
        _lang = _lang.upper()
    
        _modules.append("num2word_" + _lang)
        _modules.append("num2word_" + _lang.split("_")[0])

for _module in _modules:
    try:
        n2wmod = __import__(_module)
        break
    except ImportError:
        pass

try:
    n2w, to_card, to_ord, to_ordnum, to_year = (n2wmod.n2w, n2wmod.to_card,
                                                n2wmod.to_ord, n2wmod.to_ordnum,
                                                n2wmod.to_year)
except NameError:
    raise ImportError("Could not import any of these modules: %s"
                          % (",".join(_modules)))
