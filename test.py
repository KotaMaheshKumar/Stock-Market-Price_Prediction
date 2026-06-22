# from yahoopanel import *

# A = YahooPanel()
# values_desired = A.global_index_panel('2026-06-10')
# # print(values_desired)
import statsmodels.formula.api as smf
from scipy.stats import norm
import numbers


def percentile_and_point_function(func_type : str, value : int | float | numbers.Real, mu, sigma):
    distribution = norm(loc = mu, scale = sigma) 
    try:
        method = getattr(distribution, func_type.lower().strip())
        print(method)
        return method(value)
    except AttributeError:
        raise ValueError(f"Invalid function type '{func_type}'. Choose 'cdf', 'ppf', etc.")     

output_A = percentile_and_point_function('ppf', 0.2, 8, 1)
print(output_A)