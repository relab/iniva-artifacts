class Signature:

    def __init__(self):
        self.processesNumber = 0
        self.signatures = {}

    def __init__(self, initialId):
        self.processesNumber = 0
        self.signatures = {}
        self.signatures[initialId] = 1

    def include(self, signature):
        if signature in self.signatures:
            return True
        return False

    def subset(self, signature):
        for sig in self.signatures:
            if not signature.include(sig):
                return False
            if signature.signatures[sig] < self.signatures[sig]:
                return False
        return True

    def subtract(self, signature):
        subtracted = {}
        for sig in self.signatures:
            if signature.include(sig):
                count = self.signatures[sig] - signature.signatures[sig]
                if count > 0:
                    subtracted[sig] = count
            else:
                subtracted[sig] = self.signatures[sig]
        sub = Signature(-2)
        sub.signatures = subtracted
        return sub

    def append(self, sigs):
        for sig in sigs.signatures:
            if sig not in self.signatures:
                self.processesNumber += 1
                self.signatures[sig] = 1
            else:
                self.signatures[sig] += 1

    def isQuorom(self, committeeSize):
        if self.processesNumber >= (2/3)*committeeSize:
            return True
        return False

    def len(self):
        return len(self.signatures)

    def size(self):
        size = 0
        for sig in self.signatures:
            size += self.signatures[sig]
        return size

    def toString(self):
        list = []
        res = ""
        for sig in sorted(self.signatures):
            for i in range(self.signatures[sig]):
                list.append(str(sig))
        res = ''.join(list)
        return res
    
def size(sig:Signature)->int :
    return sig.processesNumber