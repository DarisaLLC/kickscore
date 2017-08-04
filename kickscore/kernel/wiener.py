import numpy as np

from .kernel import Kernel


VEC_ZERO = np.zeros(1)
VEC_ONE = np.ones(1)
ARRAY_ZERO = np.zeros((1, 1))
ARRAY_ONE = np.ones((1, 1))


class Wiener(Kernel):

    """Kernel of a Wiener process.

    In practice, it should probably be used in conjunction with a constant
    (a.k.a. bias) kernel so that the variance at t = 0 is positive.
    """

    def __init__(self, var, t0):
        self.var = var
        self.t0 = t0

    def k_mat(self, ts1, ts2=None):
        if ts2 is None:
            ts2 = ts1
        ts1 = np.asarray(ts1)
        ts2 = np.asarray(ts2)
        return self.var * (np.fmin(ts1[:,None], ts2[None,:]) - self.t0)

    def k_diag(self, ts):
        ts = np.asarray(ts)
        return self.var * (ts - self.t0)

    @property
    def order(self):
        return 1

    def transition(self, delta):
        return ARRAY_ONE

    def noise_cov(self, delta):
        return self.var * delta * ARRAY_ONE

    def state_mean(self, t):
        return VEC_ZERO

    def state_cov(self, t):
        return self.var * (t - self.t0) * ARRAY_ONE

    @property
    def measurement_vector(self):
        return VEC_ONE

    @property
    def feedback(self):
        return ARRAY_ZERO

    @property
    def noise_effect(self):
        return VEC_ONE

    @property
    def noise_density(self):
        return self.var
