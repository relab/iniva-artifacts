class Block:
    def __init__(self, id, content, proposer):
        self.id = id
        self.content = content
        self.signatures = []
        self.numberOfSignatures = 0
        self.proposer = proposer
        self.exNum = 0

    def isValid(self):
        return True

    def isConfirmed(self , size):
        if len(self.signatures) > (2*(size / 3)):
            return True
        return False