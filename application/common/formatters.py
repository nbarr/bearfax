# -*- coding: utf-8 -*-

import re


def safe_join(sequence, separator='', skip_list=None, skip_false=False, converter=str,
              remove_duplicated_separators=True):
    """Join sequence without fails on `None` or non-string values
       Args:
       - `sequence` - iterable of elements to join
       - `separator` - string used to join its `sequence`
       - `skip_list` - list of values that must be dropped from join
       - `skip_false` - drop from joining all elements that evaluated to boolean `False`
       - `converter` - callable that used to convert elements of `sequence` to suitable format (usually `str`)
    """

    result = ''

    try:
        if skip_list is None:
            skip_list = []

        result =  separator.join([converter(item) for item in sequence
                                  if item not in skip_list and not (skip_false and not bool(item))])

        if remove_duplicated_separators:
            result = re.sub('{}+'.format(separator), separator, result, re.IGNORECASE | re.UNICODE)

    except:
        pass

    return result
