from typing import Protocol
import numpy as np

from utils import divide_value

class Calculator_base(Protocol):
    def _yield_function(self):
        raise NotImplementedError()

    def _calculate_dsig_deps_e(self):
        raise NotImplementedError()

    def _calculate_dsig_deps_p(self):
        raise NotImplementedError()

    def _divide_eps_inc(self):
        raise NotImplementedError()

    def _calculate_sig_increment(self):
        raise NotImplementedError()


class Perfect_elastoplastic(Calculator_base):
    def __init__(self, epsilons, E, Y):
        self.E = E
        self.Y = Y
        self.epsilons = epsilons
        self.e_sigmas = np.zeros(np.shape(self.epsilons))
        self.sigmas = np.zeros(np.shape(self.epsilons))

    def init(self):
        self.e_sigmas = np.zeros(np.shape(self.epsilons))
        self.sigmas = np.zeros(np.shape(self.epsilons))

    def _yield_function(self, sigma):
        return abs(sigma) >= self.Y

    def _calculate_dsig_deps_e(self):
        return self.E

    def _calculate_dsig_deps_p(self):
        return 0.0

    def _divide_eps_inc(self, sigma, eps_inc):
        dsig_deps_e = self._calculate_dsig_deps_e()
        dsig_e = dsig_deps_e * eps_inc
        tmp_sig = sigma + dsig_e
        yield_flag = self._yield_function(tmp_sig)
        if yield_flag:
            if self._yield_function(sigma):
                return 0.0 , eps_inc
            return divide_value(eps_inc, sigma, self.Y, dsig_deps_e)
        return eps_inc, 0.0

    def _calculate_sig_increment(self, eps_e_inc, eps_p_inc):
        dsig_deps_e = self._calculate_dsig_deps_e()
        dsig_deps_p = self._calculate_dsig_deps_p()
        dsig_e = dsig_deps_e * eps_e_inc
        dsig_p = dsig_deps_p * eps_p_inc
        return dsig_e, dsig_p

    def calculate_histerisis(self):
        self.init()
        for idx in range(1, len(self.epsilons)):
            current_strain = self.epsilons[idx]
            before_strain = self.epsilons[idx - 1]
            eps_inc = current_strain - before_strain
            eps_e_inc, eps_p_inc = self._divide_eps_inc(self.sigmas[idx - 1], eps_inc)
            dsig_e, dsig_p = self._calculate_sig_increment(eps_e_inc, eps_p_inc)
            self.e_sigmas[idx] = self.e_sigmas[idx - 1] + dsig_e
            self.sigmas[idx] = self.e_sigmas[idx] + dsig_p


if __name__ == "__main__":
    from matplotlib import pyplot as plt
    from utils import create_loop
    amps = [0.05, -0.05]
    epsilons = create_loop(amps)
    perf_ep = Perfect_elastoplastic(epsilons, 205000.0, 235.0)
    perf_ep.calculate_histerisis()

    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.plot(perf_ep.epsilons, perf_ep.sigmas)
    plt.show()
    #print(perfect_ep.sigmas)