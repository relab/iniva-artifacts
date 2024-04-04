import random

class Committee:
    def __init__(self, size, users):
        self.committeeSize = size
        self.validators = users
        self.blocks = []
        self.omittedBlocks = 0
        self.proposer = self.validators[0]
        self.seed = 42
        random.seed(self.seed)

    def shuffle(self):
        pass

    def distributeRewards(self, newBlock):
        pass

    def round(self, roundNumber):
        random.seed(self.seed + roundNumber)
        self.shuffle()
        newBlock = self.proposer.propose(self.blocks)
        # print(self.proposer.__dict__)
        total = 0
        for v in self.validators:
            v.sign(newBlock)
        if newBlock.isConfirmed(self.committeeSize):
            self.blocks.append(newBlock)
            self.distributeRewards(newBlock)
            return True
        else:
            print("Invalid")
            return False