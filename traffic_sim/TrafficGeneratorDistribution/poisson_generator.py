import numpy as np
from .base_generator import BaseGenerator

class PoissonGenerator(BaseGenerator):
    def generate(self, epoch):
        return np.random.poisson(self.rate)
