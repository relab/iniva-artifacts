import random
from committee import Committee
from validator import Validator


class InivaCommittee (Committee):
    def __init__(self, size, users, fanout):
        super().__init__(size, users)
        self.fanout = fanout
        self.leafCount = int((size - 1 - fanout)/ fanout)
        self.leaderBonus = 0.15
        self.aggregationBonus = 0.0005
        #self.aggregationBonus = 0
        self.blockReward = 10000

    def shuffle(self):
        random.shuffle(self.validators)
        self.proposer = self.validators[0]
        for v in self.validators:
            v.currentRole = "Member"
            v.secondChance = False
            v.children = []
        self.validators[0].currentRole = "Leader"
        self.validators[0].parent = None
        for i in range(1, self.fanout + 1):
            self.validators[i].currentRole = "Aggregator"
            self.validators[i].parent = self.validators[0]
            initial = (self.leafCount * (i-1)) + self.fanout+ 1
            end = initial + self.leafCount
            for j in range(initial, end):
                self.validators[j].parent = self.validators[i]
                self.validators[i].children.append(self.validators[j])

    def distributeRewards(self, newBlock):
        for v in newBlock.signatures:
            v.attack(newBlock, self.blocks)
        count = len(newBlock.signatures)
        maxfault = int(self.committeeSize / 3)
        threshold = self.committeeSize - maxfault
        leaderBonus = ((count - threshold) / maxfault) * self.leaderBonus * self.blockReward
        fullLeaderBonus = self.leaderBonus * self.blockReward
        aggregationBonus = 0
        fullAggregationBonus = 0
        for i in range(len(self.validators)):
            v = self.validators[i]
            if v.currentRole == "Aggregator" and v in newBlock.signatures:
                for v2 in v.children:
                    fullAggregationBonus += self.aggregationBonus * self.blockReward
                    if v2 in newBlock.signatures and not v2.secondChance:
                        aggregationBonus += self.aggregationBonus * self.blockReward
                        v.reward += self.aggregationBonus * self.blockReward
            if v.currentRole == "Leader":
                v.reward += leaderBonus
        votingReward = self.blockReward - fullLeaderBonus - fullAggregationBonus
        punishments = 0
        for v in newBlock.signatures:
            if v.secondChance:
                v.reward += ((votingReward / len(newBlock.signatures)) - (self.aggregationBonus * self.blockReward))
                punishments += (self.aggregationBonus * self.blockReward)
            else:
                v.reward += votingReward / len(newBlock.signatures)
        divisable = (fullLeaderBonus - leaderBonus) + (fullAggregationBonus - aggregationBonus) + punishments
        for v in self.validators:
            v.reward += divisable / len(self.validators)
