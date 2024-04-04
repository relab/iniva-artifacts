from signature import Signature
import random
import copy

class Process:

    def __init__(self, id):
        self.id = id
        self.signature = Signature(id)

    def receive(self, sig):
        if not sig.subset(self.signature):
            self.signature.append(sig)

    def send(self, k, committee):
        samples = []
        while(True):
            samples = random.sample(committee, k)
            if self not in samples:
                break
        receivers = []
        for sample in samples:
            x = copy.deepcopy(self.signature)
            receivers.append((sample, x))
        return receivers

    def sendTo(self, receiver):
        x = copy.deepcopy(self.signature)
        return (receiver, x)

    def hasQuorom(self, size):
        if self.signature.isQuorom(size):
            #print(self.signature.signatures)
            return True
        return False