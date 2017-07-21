import sys
import json
import api_routines
import lmfdb_api

from ell_lmfdb import EllipticCurve_rational_field_lmfdb

URL_API = lmfdb_api.URL_BASE + 'api/elliptic_curves/curves/?_format=json&'

#sage-name, lmfdb-name, lmfdb-data-type
Translation = [['label', 'label', 'string'],
               ['degree', 'degree', 'int'],
               ['conductor', 'conductor', 'int'],
               ['torsion_order', 'torsion', 'int'],
               ['rank', 'rank', 'int'],
               ['regulator', 'regulator', 'float'],
              ]

Not_implemented = ['min_conductor', 'max_conductor']

def search(**kwargs):
    r"""
    Search the LMFDB for an elliptic curve.

    Note that all inputs are optional, but at least one input is necessary.

    INPUT:

    -  ``label=l`` -- a string ``l`` representing a label in the LMFDB.

    -  ``degree=d`` -- an int ``d`` giving the minimum degree of a
       parameterization of the modular curve

    -  ``conductor=c`` -- an int ``c`` giving the conductor of the curve

    -  ``min_conductor=mc`` -- an int ``mc`` giving a lower bound on the
       conductor for desired curves

    -  ``max_conductor=mc`` -- an int ``mc`` giving an upper bound on the
       conductor for desired curves

    -  ``torsion_order=t`` -- an int ``t`` giving the order of the torsion
       subgroup of the curve

    -  ``rank=r`` -- an int ``r`` giving the rank of the curve

    -  ``regulator=f`` -- a float ``f`` giving the regulator of the curve

    -  ``max_items=m`` -- an int ``m`` (default: 10, max: 100) indicating the
       maximum number of results to return

    -  ``base_item=b`` -- an int ``b`` (default: 0) specifying where to start
       returning values from. The search will begin by returning the ``b``th
       curve. Combined with ``max_items`` to return data in chunks.

    -  ``sort=s`` -- a string ``s`` specifying what database field to sort the
       results on. See the LMFDB api for more info.

    EXAMPLES::

        sage: Es = search(conductor=11050, rank=2)
        [Elliptic Curve defined by y^2 + x*y = x^3 - x^2 - 442*x + 1716 over Rational Field, Elliptic Curve defined by y^2 + x*y = x^3 - x^2 + 1558*x + 11716 over Rational Field]
        sage: E = E[0]
        sage: E.conductor()
        11050
    """
    searches = []
    try:
        kwargs['label']
        kwargs['single_field'] = True
    except KeyError:
        pass

    for item in Not_implemented:
        try:
            kwargs[item]
            raise NotImplementedError("This would be a great thing to have, " +
                "but the LMFDB api does not yet provide this functionality.")
        except KeyError:
            pass

    for item in Translation:
        try:
            searches.append(_construct_search(item, **kwargs))
            del kwargs[_sage_name(item)]
        except KeyError:
            pass

    try:
        sort = searches.append('_sort=' + kwargs['sort'])
    except KeyError:
        pass

    if len(searches) == 0:
        print("No searches recognized. No data will be returned.")
        return None

    dbfields = ['label',
                'degree',
                'conductor',
                'xainvs',
                'torsion',
                'regulator',
                'x-coordinaates_of_integral_points',
                'gens',
                'lmfdb_label',
                'rank'
                ]
    fields = lmfdb_api._get_fields_from_api_page(URL_API, searches, dbfields,
                        EllipticCurve_rational_field_lmfdb, **kwargs)
    return fields


def _sage_name(trans):
    return trans[0]

def _lmfdb_name(trans):
    return trans[1] + '='

def _lmfdb_type(trans):
    return trans[2]

def _construct_search(trans, **kwargs):
    routine = api_routines.api_selector(_lmfdb_type(trans))
    return _lmfdb_name(trans) + routine(kwargs[_sage_name(trans)])
