class Stack:
    def __init__(self):
        self.stack_list = []

    def push(self, element):
        self.stack_list.append(element)

    def pop(self):
        if len(self.stack_list) > 0:
            ret_el = self.stack_list[-1]
            del self.stack_list[-1]
            return ret_el

    def __len__(self):
        return len(self.stack_list)
