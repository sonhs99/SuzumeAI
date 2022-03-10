from .five import FivePlaneEncoder

encoder_list = [
    FivePlaneEncoder
]

def selector(encoder_name):
    for encoder in encoder_list:
        if encoder.name() == encoder_name:
            return encoder()
    return None