from .small import *
from .resnet import *

network_list = [
    SmallNetwork,
    ResnetNetwork,
]

def selector(network_name):
    for network in network_list:
        if network.name() == network_name: return network
    return None