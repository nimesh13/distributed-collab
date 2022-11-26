from time import time
from clock import Clock

class HLC:
    def __init__(self, pt: time, nodeid: str, lt: int=0) -> None:
        self.clock = Clock(pt, lt)
        self.nodeid = nodeid
    
    def __str__(self):
        return str(self.clock.pt) + ':' + str(self.clock.lt) + ':' + str(self.nodeid)
    
    def incr(self, now) -> None:
        if now > self.clock.pt:
            self.clock.pt = now
            self.clock.lt = 0
        else:
            self.clock.lt += 1
        return self

    def cmpr(self, message) -> int:
        if self.clock.pt == message.clock.pt:
            if self.clock.lt == message.clock.lt:
                if self.nodeid == message.nodeid:
                    return 0
                return -1 if self.nodeid < message.nodeid else 1
            return self.clock.lt - message.clock.lt
        return self.clock.pt - message.clock.pt
    
    def event(self, now) -> None:
        self.incr(now)

    def receive(self, message, now) -> None:
        if now > self.clock.pt and now > message.clock.pt:
            self.clock.pt = now
            self.clock.lt = 0
            return
        if self.clock.pt == message.clock.pt:
            self.clock.lt = max(self.clock.lt, message.clock.lt + 1)
        elif self.clock.pt > message.clock.pt:
            self.clock.lt += 1
        else:
            self.clock.pt = message.clock.pt
            self.clock.lt = message.clock.lt + 1
    
    @staticmethod
    def unmarshal(message: str):
        split = message.split(':')
        return HLC(int(split[0]), split[2], int(split[1]))