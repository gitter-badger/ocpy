class RAMONBase(object):
    """
    RAMONBase Object for storing neuroscience data

    Attributes:
        :data:      ``numpy.array`` The voxel data for a RAMON object

    """
    def __init__(self, arg):
        super(ramon, self).__init__()
        self.arg = arg
