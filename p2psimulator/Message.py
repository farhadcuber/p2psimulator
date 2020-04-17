class Message:
    def __init__(self, sender, receiver, type, data, size, time=0):
        self.type = type
        self.sender = sender
        self.receiver = receiver
        self.data = data
        self.size = size
        self.time = time

    def __eq__(self, other):
        if other == None:
            return False
        return self.time == other.time

    def __lt__(self, other):
        return self.time < other.time