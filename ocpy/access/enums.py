DEFAULT_PROTOCOL =  'http'
DEFAULT_SERVER =    'http://openconnecto.me'
DEFAULT_FORMAT =    'hdf5'
CHUNK_DEPTH    =    16

class DataSizeError(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg
