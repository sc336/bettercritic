import scipy.stats as stats
import scipy.stats._continuous_distns as continuous_distns
import numpy as np
import math

# ISSUES
# truncnorm_gen and skewnorm_gen use parameter 'a' to mean different things - skewnorm is non-standard in that it uses it for skew.
#  - Appears this is not a problem, it looks as if that 'a' is only used locally.
# Looks like rv_continuous.ppf() passes scale and loc (and all other arguments) to _ppf - see line 1991-1993 of _distn_infrastructure.py
#  but only passes scale to _pdf (1729-1731)
# -Small difference between this and truncnorm's ppf, seemingly after 12dp.  Calculations are numeric, so small differences
#   in implementation could cause this kind of discrepancy without being wrong.

#TODO: Proper testing

class trunc_skew_norm_gen(continuous_distns.skew_norm_gen):

    def __init__(self, momtype=1, a=None, b=None, xtol=1e-14, badvalue=None, name=None, longname=None, shapes=None, extradoc=None, seed=None):
        super().__init__(momtype=1, a=None, b=None, xtol=1e-14, badvalue=None, name=None, longname=None, shapes=None, extradoc=None, seed=None)
        self._amin_cache = math.nan
        self._bmax_cache = math.nan

    def _argcheck(self, a, b, skew):
        return (a < b) & np.isfinite(skew)

    def _get_support(self, a, b, *args, **kwds):
        return a, b

    def _get_norms_cached(self, a, b, skew):
        #Numeric integrals inside numeric integrals are REALLY slow.
        # Therefore, some very very simple caching of the normalising values
        if not (math.isnan(self._amin_cache)
            or math.isnan(self._bmax_cache)):
            if self._amin_cache == a and self._bmax_cache == b:
                if not (math.isnan(self._na_cache)
                    or math.isnan(self._nb_cache)
                    or math.isnan(self._sa_cache)
                    or math.isnan(self._sb_cache)
                    or math.isnan(self._delta_cache)):
                        return self._na_cache, self._nb_cache, self._sa_cache, self._sb_cache, self._delta_cache, np.log(self._delta_cache)

        self._amin_cache = a
        self._bmax_cache = b
        self._na_cache, self._nb_cache, self._sa_cache, self._sb_cache, self._delta_cache, throw_away = self._get_norms(a, b, skew)
        return self._na_cache, self._nb_cache, self._sa_cache, self._sb_cache, self._delta_cache, np.log(self._delta_cache)

    def _get_norms(self, a, b, skew):
        # Adapted from the _get_norms() function of stats.truncnorm

        # This is where we calculate the integral under the included section, with which to normalise our function.

        # TODO: replace with internal calls from super() (low priority)
        # truncnorm calls _normcdf and _norm_sf (which is just the right tailed cdf, afaict)
        # what would be the equivalent for skewnorm?
        _nb = stats.skewnorm.cdf(b, skew)
        _na = stats.skewnorm.cdf(a, skew)
        _sb = stats.skewnorm.cdf(b, skew)
        _sa = stats.skewnorm.cdf(a, skew)
        _delta = np.where(a > 0, _sa - _sb, _nb - _na)
        with np.errstate(divide='ignore'):
            return _na, _nb, _sa, _sb, _delta, np.log(_delta)

    def _pdf(self, x, a, b, skew):
        # BEWARE
        # It seems the x parameter is transformed for location and scale.
        # a,b are passed in transformed by the user.
        # The documentation examples (https://scipy.github.io/devdocs/generated/scipy.stats.skewnorm.html)
        #  indicate that skew can be passed in without scale transformation.
        if a < x < b:
            ans = self._get_norms_cached(a, b, skew)
            _delta = ans[4]

            return super()._pdf(x, skew) / _delta
        else:
            return 0
