import random
from committee import Committee
from validator import Validator


class CosmosCommittee (Committee):
    def __init__(self, size, users, fanout):
        super().__init__(size, users)
        self.leaderBonus = 0.18
        self.blockReward = 10000

    def shuffle(self):
        random.shuffle(self.validators)
        self.proposer = self.validators[0]
        for v in self.validators:
            v.currentRole = "Member"
        self.validators[0].currentRole = "Leader"

    def distributeRewards(self, newBlock):
        for v in newBlock.signatures:
            v.attack(newBlock, self.blocks)
        count = len(newBlock.signatures)
        maxfault = int(self.committeeSize / 3)
        threshold = self.committeeSize - maxfault
        leaderBonus = ((count - threshold) / maxfault) * self.leaderBonus * self.blockReward
        votingReward = self.blockReward - leaderBonus
        for v in newBlock.signatures:
            v.reward += votingReward / len(newBlock.signatures)
            if v.currentRole == "Leader":
                v.reward += leaderBonus
