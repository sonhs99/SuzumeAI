class Encoder:
    def __init__(self):
        pass

    def encode(self, state, idx):
        raise NotImplementedError()

    def size(self):
        raise NotImplementedError()

    @staticmethod
    def name():
        return 'Not Implemented'
