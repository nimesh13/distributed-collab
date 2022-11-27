from json import dumps

class Message:
    def __init__(self, msgid: str, add: dict, remove: dict, ts: str) -> None:
        self.msg_id = msgid
        self.add = add
        self.remove = remove
        self.ts = ts
    
    def toJSON(self):
        return dumps(self, default=lambda o: o.__dict__, 
        sort_keys=True, indent=4)