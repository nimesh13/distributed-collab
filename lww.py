class LWW:
    def __init__(self) -> None:
        self.add = {}
        self.remove = {}
    
    def addSet(self, element, ts) -> bool:
        operation = False
        present_in_add_set = element in self.add
        present_in_remove_set = element in self.remove

        if not present_in_add_set and not present_in_remove_set:
            self.add[element] = ts
            operation = True
        elif present_in_add_set and ts > self.add[element]:
            self.add[element] = ts
            operation = True
        elif present_in_remove_set and ts > self.remove[element]:
            del self.remove[element]
            self.add[element] = ts
            operation = True

        return operation

    def removeSet(self, element, ts) -> bool:
        operation = False
        present_in_add_set = element in self.add
        present_in_remove_set = element in self.remove

        if not present_in_add_set and not present_in_remove_set:
            self.remove[element] = ts
            operation = True
        elif present_in_remove_set and ts > self.remove[element]:
            self.remove[element] = ts
            operation = True
        elif present_in_add_set and ts > self.add[element]:
            del self.add[element]
            self.remove[element] = ts
            operation = True

        return operation