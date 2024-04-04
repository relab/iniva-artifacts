from validator import Validator

class CosmosValidator (Validator):
    def __init__(self, id, type, group=0, target=0, attackSteal=False, attackOmission=False, attackForce=False, attackNoVote = False, colatural=1):
        super().__init__(id, type, group, target, attackSteal, attackOmission, attackForce, attackNoVote, colatural)

    def attack(self, block, blocks):
        if self.type == "Byzantine":
            if self.attackOmission:
                self.omitVote(block, blocks)
            if self.attackNoVote:
                self.noVote(block)

    def omitVote(self, block, blocks):
        if self.currentRole == "Leader":
            block.signatures.remove(self.target)

    def noVote(self, block):
        if self.target.currentRole == "Leader":
            block.signatures.remove(self)
