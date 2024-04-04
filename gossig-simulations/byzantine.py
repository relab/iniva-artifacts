from process import Process
from itertools import chain, combinations
import copy
from signature import size as sigsize

class Byzantine(Process):

    def __init__(self, id, victims, colateral):
        Process.__init__(self, id)
        self.victims = victims
        self.colateral = colateral
        self.individualShares = []
        x = copy.deepcopy(self.signature)
        self.individualShares.append(x)
        self.extractedShares = {}
        self.extractedShares[x.toString()] = x
        self.extracted = {}
        for victim in victims:
            self.extracted[victim] = False

    def receive(self, sig):
        Process.receive(self,sig)
        x = copy.deepcopy(sig)
        self.individualShares.append(x)
        self.extract(copy.deepcopy(sig))
        self.signature.append(sig)

    def extract(self, sigg):
        #print(sigg.size())
        maxSize = 12
        #if sigg.size() > maxSize:
        #    return self.allVictimsExtractedwithColateral()
        #self.extractedShares[sigg.toString()] = sigg
        
        #substract extracted singleton shares
        for share in self.extractedShares:
            shareSig = self.extractedShares[share]
            if shareSig.processesNumber > 1 or shareSig.size() > 1:
                continue
            while (shareSig.subset(sigg) and shareSig.toString() != sigg.toString()):
                sigg = sigg.subtract(shareSig)
        
        #substract any subset if size is above maxSize
        if sigg.size() > maxSize:
            for share in self.extractedShares:
                shareSig = self.extractedShares[share]
                while (shareSig.subset(sigg) and shareSig.toString() != sigg.toString()):
                    sigg = sigg.subtract(shareSig)
        
        queue = [sigg]
        while(len(queue) > 0):

            if len(queue) > 2* len(self.extractedShares):
                print("Queue too big, size ", len(queue))

            for victim in self.victims:
                if str(victim) in self.extractedShares:
                    self.extracted[victim] = True
            if self.allVictimsExtractedwithColateral():
                return True
            sig = queue.pop()
            exs = {}
            
            extractedPart = False
            remove = []
            for share in self.extractedShares:
                shareSig = self.extractedShares[share]
                extracted = None
                if shareSig.subset(sig) and shareSig.toString() != sig.toString():
                    extracted = sig.subtract(shareSig)
                    extractedPart = True
                elif sig.subset(shareSig) and shareSig.toString() != sig.toString():
                    extracted = shareSig.subtract(sig)
                    remove.append(share)
                if extracted is not None:
                    if extracted.toString() not in self.extractedShares:
                        if extracted.size() < maxSize:
                            exs[extracted.toString()] = extracted
                        #print(extracted.toString())
                #if len(self.extractedShares) > 15000:
                    #return self.allVictimsExtractedwithColateral()
            if not extractedPart and sig.size() < maxSize:
                # we did not find any substing, so lets add this
                self.extractedShares[sig.toString()] = sig
            for ex in exs:
                queue.append(exs[ex])
            for share in remove:
                # we found a substring. If we have a and b, no point in keeping a+b
                del self.extractedShares[share]
            
        return self.allVictimsExtractedwithColateral()

    def allVictimsExtracted(self):
        for victim in self.victims:
            if not self.extracted[victim]:
                return False
        return True
    
    def allVictimsExtractedwithColateral(self):
        for victim in self.victims:
            if self.extracted[victim]:
                continue
            extracted = False
            if self.colateral == 0:
                return False
            for sig in self.extractedShares.values():
                if sig.size() > self.colateral+1:
                    continue
                if sig.include(victim):
                    extracted = True
                    break
            if not extracted:
                return False
        return True

    def powerset(self, iterable):
        "powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
        return chain.from_iterable(combinations(iterable, r) for r in range(1, len(iterable) + 1))