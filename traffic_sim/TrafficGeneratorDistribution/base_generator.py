class BaseGenerator:
    def __init__(self, rate):
        self.rate = rate
        
    def generate(self, epoch):
        raise NotImplementedError("Subclasses must implement generate()")
