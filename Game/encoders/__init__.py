from json import encoder
from .four import FourEncoder

def selector(encoder_name):
    if encoder_name == 'four':
        return FourEncoder()
    return None