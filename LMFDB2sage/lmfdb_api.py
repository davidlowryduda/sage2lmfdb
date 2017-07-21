"""
Basic lmfdb api, taken from Chris Brady's pylmfdb.
"""

import api_routines

try:
    from six.moves.urllib.request import urlopen
except:
    raise ImportError('Unable to find six compatability layer. Aborting')

try:
    import json
except:
    raise ImportError('Unable to import json parser')


URL_BASE = 'http://beta.lmfdb.org/'


def _get_fields_from_api_page(base_url, requests, db_fields, object_base, **kwargs):
    full_url = base_url + api_routines.api_amp_list(requests) + "&" + \
               "_fields="+api_routines.api_comma_list(db_fields)
    try:
        offset = int(kwargs['base_item'])
        full_url += "&_offset="+str(offset)
    except:
        pass

    try:
        single_field = kwargs['single_field']
        #This is a bit of a hack. Set the 'max_items' keyword to 2, so that you can detect
        #if the database returns more than one item, but so that you don't drag out too much
        #unnecessary data
        kwargs['max_items'] = 2
    except:
        single_field = False

    fields = []
    count = 0
    max_count = None
    try:
        max_count = int(kwargs['max_items'])
    except:
        max_count = 10
    while True:
        try:
            page = urlopen(full_url)
            result = json.loads(page.read())
        except:
            break
        count_this_page = int(result['offset']) - int(result['start'])
        count += count_this_page
        for c in result['data']:
            fields.append(object_base(c))
        if count_this_page < 100:
            break
        if max_count is not None:
            if count >= max_count:
                break
        full_url = URL_BASE + result['next']

    if len(fields) == 0:
        print("No fields were found satisfying input criteria.")
        return
    if single_field:
        if len(fields) != 1:
            print('Warning! Code is returning a single field, but database returned more than one')
        return fields[0]
    if max_count is not None:
        return fields[ : min(len(fields),max_count)]
    return fields
