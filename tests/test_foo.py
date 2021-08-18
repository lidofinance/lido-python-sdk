import pytest
import numpy as np

import mypackage.foo


@pytest.mark.parametrize("dim", [3, 4, 5])
def test_a_function(dim):

    output = mypackage.foo.a_function(x=0.0, dim=dim)

    pass_conditions = output == pytest.approx(np.ones(dim))
    if not pass_conditions:
        raise AssertionError()
