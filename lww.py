from hlc import HLC
from utils import getEvent
from json import dumps

class LWW:
    def __init__(self, add={}, remove={}) -> None:
        self.add = add
        self.remove = remove
    
    def querySet(self, set, element: str) -> bool:
        return element in set
    
    def addSet(self, element: str, ts: HLC) -> bool:
        operation = False
        present_in_add_set = self.querySet(self.add, element)
        present_in_remove_set = self.querySet(self.remove, element)

        if not present_in_add_set and not present_in_remove_set:
            self.add[element] = ts
            operation = True
        elif present_in_add_set and self.add[element].cmpr(ts) < 0:
            self.add[element] = ts
            operation = True
        elif present_in_remove_set and self.remove[element].cmpr(ts) < 0:
            del self.remove[element]
            self.add[element] = ts
            operation = True

        return operation

    def removeSet(self, element: str, ts: HLC) -> bool:
        operation = False
        present_in_add_set = self.querySet(self.add, element)
        present_in_remove_set = self.querySet(self.remove, element)

        if not present_in_add_set and not present_in_remove_set:
            self.remove[element] = ts
            operation = True
        elif present_in_remove_set and self.remove[element].cmpr(ts) < 0:
            self.remove[element] = ts
            operation = True
        elif present_in_add_set and self.add[element].cmpr(ts) < 0:
            del self.add[element]
            self.remove[element] = ts
            operation = True

        return operation
    
    def merge(self, add, remove) -> bool:
        operation = False
        for element, ts in add.items():
            noop = self.addSet(element, ts)
            if noop and not operation:
                operation = True
        for element, ts in remove.items():
            noop = self.removeSet(element, ts)
            if noop and not operation:
                operation = True
        
        return operation
    
    def setToJSONArr(self):
        output= []
        for event, ts in self.add.items():
            output.append(getEvent(event, str(ts)))
        
        sorted(output, key=lambda x: x['ts'])
        return dumps(output)
    
    @staticmethod
    def toJSON(set):
        output = {}
        for event, ts in set.items():
            output[event] = str(ts)
        
        return output
    
    @staticmethod
    def fromJSON(msg_add, msg_remove):
        add, remove = {}, {}
        for event, ts in msg_add.items():
            add[event] = HLC.unmarshal(ts) 
        for event, ts in msg_remove.items():
            remove[event] = HLC.unmarshal(ts)
        
        return LWW(add, remove)