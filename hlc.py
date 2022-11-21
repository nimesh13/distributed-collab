from clock import Clock

class HLC:
    def __init__(self, clock: Clock, nodeid) -> None:
        self.clock = clock
        self.nodeid = nodeid
    
    def marshal(self):
        return self.clock.pt + ':' + self.clock.lt + ':' + self.nodeid
    
    def unmarshal(self, message: str):
        split = message.split(':')
        self.clock = Clock(split[0], split[1])
        self.nodeid = split[2]
        return self
    
    def incr(self, now) -> None:
        if now > self.clock.pt:
            self.clock.pt = now
            self.clock.lt = 0
        else:
            self.clock.lt += 1

    def cmpr(self, message) -> int:
        if self.clock.pt == message.pt:
            if self.clock.lt == message.lt:
                if self.nodeid == message.nodeid:
                    return 0
                return -1 if self.nodeid < message.nodeid else 1
            return self.clock.lt - message.lt
        return self.clock.pt - message.pt
    
    def event(self, now) -> None:
        self.incr(now)

    def receive(self, message, now) -> None:
        if now > self.clock.pt and now > message.pt:
            self.clock.pt = now
            self.clock.lt = 0
            return
        if self.clock.pt == message.pt:
            self.clock.lt = max(self.clock.lt, message.lt + 1)
        elif self.clock.pt > message.pt:
            self.clock.lt += 1
        else:
            self.clock.pt = message.pt
            self.clock.lt = message.lt + 1