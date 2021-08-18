"""
A generic module to use as example.
"""

import numpy as np


def a_function(x, dim):
    """
    Define a generic function.

    :param float x:
        The function's argument array.

    :param int dim:
        Number of dimensions to expand.

    :return:
        The evaluated function at the given input array.
    :rtype: float
    """
    f = np.ones(dim) + x
    return f
