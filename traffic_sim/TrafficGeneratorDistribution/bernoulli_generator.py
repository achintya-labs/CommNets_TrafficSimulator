import random
from .base_generator import BaseGenerator

class BernoulliGenerator(BaseGenerator):
    def generate(self, epoch):
        if random.random() < self.rate:
            return 1
        return 0
