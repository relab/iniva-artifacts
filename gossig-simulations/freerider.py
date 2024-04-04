from process import Process

class FreeRider(Process):
    """The FreeRider Process 
    overwrites the receive method.
    Does only receive signatures once, then keeps sending the same signature.
    """

    def __init__(self, id, maxParticipation):
        Process.__init__(self, id)
        self.maxParticipation = maxParticipation
        self.countParticipation = 0
        self.received = False

    def receive(self, sig):
        if not self.received:
            Process.receive(self,sig)
            self.received = True