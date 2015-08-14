from enums import *
from exceptions import *

import RAMONBase

class RAMONVolume(RAMONBase):
    """
    RAMONVolume Object for storing neuroscience data with a voxel volume
    """
    def __init__(self,  id = DEFAULT_ID,
                        confidence = DEFAULT_CONFIDENCE,
                        dynamic_metadata = DEFAULT_DYNAMIC_METADATA,
                        status = DEFAULT_STATUS,
                        author = DEFAULT_AUTHOR):
        """
        Initialize a new RAMONVolume object. Inherit default attributes from RAMONBase,
        as well as:

        Arguments:
            :data:              `number[]` Voxel volume
        """

        self._data = data

        RAMONBase.__init__(self, id=id, confidence=confidence,
                         dynamic_metadata=dynamic_metadata,
                         status=status, author=author)
