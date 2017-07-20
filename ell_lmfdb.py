
from sage.schemes.elliptic_curves.ell_rational_field import EllipticCurve_rational_field
import ast

class EllipticCurve_rational_field_lmfdb(EllipticCurve_rational_field):
    def __init__(self,json):
        self._json = json
        ainvs = ast.literal_eval(json['xainvs'])
        EllipticCurve_rational_field.__init__(self,ainvs)
        if 'conductor' in json:
            # If we wanted to be parallel to sage, we might try to do:
            #self._set_conductor(json['conductor'])
            self._lmfdb_conductor = json['conductor']
            # But this runs much slower.
        if 'x-coordinates_of_integral_points' in json:
            self._lmfdb_x_integral_points=ast.literal_eval(json['x-coordinates_of_integral_points'])
        if  'rank' in json:
            # Interestingly, this yields very quick evaluation
            self._set_rank(json['rank'])
            #self._lmfdb_rank = json['rank']
        if 'degree' in json:
            self._set_modular_degree(json['degree'])
        if 'gens' in json:
            self._set_gens([map(int, P[1:-1].split(":")) for P in json['gens']])
        if 'lmfdb_label' in json:
            self._lmfdb_label = json['lmfdb_label']
        if 'torsion' in json:
            self._set_torsion_order(json['torsion'])
        if 'regulator' in json:
            self._lmfdb_regulator=float(json['regulator'])

    # With sample documentation note
    def regulator(self,**kwargs):
        r"""
        Return the regulator of the curve. This is taken from the lmfdb if available.

        NOTE:
            In later implementations, this docstring will probably include the
            docstring from sage's regular implementation. But that's not
            currently the case.
        """
        try:
            return self._lmfdb_regulator
        except AttributeError:
            return super(EllipticCurve_rational_field_lmfdb, self).regulator(**kwargs)

#    def rank(self, **kwargs):
#        try:
#            return self._lmfdb_rank
#        except AttributeError:
#            print("Exception")
#            return super(EllipticCurve_rational_field_lmfdb,self).rank(**kwargs)

    def conductor(self, **kwargs):
        try:
            return self._lmfdb_conductor
        except AttributeError:
            return super(EllipticCurve_rational_field_lmfdb,self).conductor(**kwargs)

    def integral_points(self, mw_base='auto', both_signs=False, verbose=False):
        try:
            x_int_points = self._lmfdb_x_integral_points
            # Now we have all the x-coordinates of integral points, and we
            # construct the points, depending on the parameter both_signs:
            if both_signs:
                int_points = sum([self.lift_x(x,all=True) for x in x_int_points],[])
            else:
                int_points = [self.lift_x(x) for x in x_int_points]
            int_points.sort()
            if verbose:
                print('Total number of integral points:',len(int_points))
            return int_points
        except AttributeError:
            return super().integral_points(self,mw_base='auto', both_signs=False, verbose=False)

