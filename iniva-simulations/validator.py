import random
from block import Block

class Validator:
    def __init__(self, id, type, group=0, target=0, attackSteal=False, attackOmission=False, attackForce=False, attackNoVote = False, colatural=1):
        self.id = id
        self.type = type
        self.reward = 0
        self.proposedBlocks = []
        self.target = target
        self.group = group
        self.attackSteal = attackSteal
        self.attackOmission = attackOmission
        self.attackForce = attackForce
        self.attackNoVote = attackNoVote
        self.currentRole = "Member"
        self.colatural = colatural


    def propose(self, blocks):
        r = random.randint(0, 100)
        b = Block(len(blocks), r, self)
        self.proposedBlocks.append(b)
        return b


    def sign(self, NewBlock):
        if NewBlock.isValid():
            NewBlock.signatures.append(self)

    def attack(self, block, blocks):
        pass


