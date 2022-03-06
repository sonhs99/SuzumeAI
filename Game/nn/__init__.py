from .small import *

def selector(network_name):
    if network_name == 'small':
        return SmallNetwork()
    return None