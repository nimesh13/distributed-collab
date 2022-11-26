from ast import dump
from hlc import HLC
from json import dumps

class Message:
    def __init__(self, msgid, add, remove, ts: HLC) -> None:
        self.messageid = msgid
        self.add = add
        self.remove = remove
        self.ts = ts
    
    def toJSON(self):
        return dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)