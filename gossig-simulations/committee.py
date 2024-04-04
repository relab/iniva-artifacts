from process import Process
from byzantine import Byzantine
from freerider import FreeRider
import random
import copy

class Committee:

    def __init__(self, size, m, fr, frmax, k, greedyMode, simType, colateral):
        self.m = m
        self.fr = fr
        self.byzantineNumber = (int)(m* size)
        self.freeRidersNumber = (int)(fr * size)
        self.correctNumber = size - (self.byzantineNumber + self.freeRidersNumber)
        self.size = size
        self.k = k
        self.validators = []
        self.greedyMode = greedyMode
        self.simType = simType
        self.extractedShares = {}

        j = 0
        for i in range(self.correctNumber):
            self.validators.append(Process(j))
            j+=1
        for i in range(self.freeRidersNumber):
            self.validators.append(FreeRider(j, frmax))
            j+=1
        for i in range(self.byzantineNumber):
            self.validators.append(Byzantine(j, [0], colateral))
            j+=1

    def allVictimsExtracted(self):
        for v in self.validators:
            if isinstance(v, Byzantine):
                if v.allVictimsExtractedwithColateral():
                    return True
        return False

    def printextracted(self):
        for v in self.validators:
            if isinstance(v, Byzantine):
                print("extracted shares: ", v.extractedShares.keys())
                break

    def exchangeShares(self, sender):
        for v in self.validators:
            if isinstance(v, Byzantine):
                for share in sender.extractedShares:
                    if share not in v.extractedShares:
                        v.extractedShares[share] = sender.extractedShares[share]

    def countIncludedFreeriders(self, finalSignature):
        count = 0
        for v in self.validators:
            if isinstance(v, FreeRider):
                if finalSignature.include(v.id):
                    count += 1
        return count / self.freeRidersNumber
    
    def extractIndividuals(self):
        for v in self.validators:
            if isinstance(v, Byzantine):
                x = copy.deepcopy(v.signature)
                self.extractedShares[x.toString()] = x

    def start(self):
        if self.simType == "Byzantine":
            return self.startByzantine()
        elif self.simType == "Freeriding":
            return self.startFreeriding()

    def startByzantine(self):
        #print("starting byzantine experiment")
        self.extractIndividuals()
        samples = random.sample(self.validators, 1)
        leader = samples[0]

        if not isinstance(leader, Byzantine):
            return False

        queue = []

        messages = []
        if self.greedyMode:
            messages = leader.send(self.k-len(leader.victims), self.validators)
            for victim in leader.victims:
                messages.append(leader.sendTo(self.validators[victim]))
        else:
            messages = leader.send(self.k , self.validators)

        for tuple in messages:
            queue.append(tuple)

        while(True):
            if self.allVictimsExtracted():
                #print("victim extracted")
                return True
            if leader.hasQuorom(self.size):
                #print("quorum collected but queue has length: ", len(queue))
                while len(queue)>0:
                    if self.allVictimsExtracted():
                        return True
                    (receiver , sig) = queue.pop(0)
                    if isinstance(receiver, Byzantine):
                        receiver.extractedShares = self.extractedShares
                    receiver.receive(sig)
                    if isinstance(receiver, Byzantine):
                        self.extractedShares = receiver.extractedShares
                        #self.printextracted()
                    #    self.exchangeShares(receiver)
                    
                return self.allVictimsExtracted()

            (receiver , sig) = queue.pop(0)
            #print(sig.signatures)
            
            if isinstance(receiver, Byzantine):
                receiver.extractedShares = self.extractedShares
            receiver.receive(sig)
            if isinstance(receiver, Byzantine):
                self.extractedShares = receiver.extractedShares
                #self.printextracted()
                #print("leader signatures: ",leader.signature.signatures)
            #    self.exchangeShares(receiver)
            messages = receiver.send(self.k, self.validators)
            for tuple in messages:
                queue.append(tuple)

    def startFreeriding(self):
        samples = random.sample(self.validators, 1)
        leader = samples[0]

        queue = []

        messages = leader.send(self.k, self.validators)

        for tuple in messages:
            queue.append(tuple)

        while (True):
            if leader.hasQuorom(self.size):
                return self.countIncludedFreeriders(leader.signature)

            (receiver, sig) = queue.pop(0)
            receiver.receive(sig)
            messages = receiver.send(self.k, self.validators)
            for tuple in messages:
                queue.append(tuple)