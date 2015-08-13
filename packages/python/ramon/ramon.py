
DEFAULT_ID                  = -1
DEFAULT_CONFIDENCE          = 00
DEFAULT_DYNAMIC_METADATA    = {}
DEFAULT_STATUS              = ''
DEFAULT_AUTHOR              = ''

class RAMONBase(object):
    """
    RAMONBase Object for storing neuroscience data
    """
    def __init__(self,  id = DEFAULT_ID,
                        confidence = DEFAULT_CONFIDENCE,
                        dynamic_metadata = DEFAULT_DYNAMIC_METADATA,
                        status = DEFAULT_STATUS,
                        author = DEFAULT_AUTHOR):
        """
        Initialize a new RAMONBase object with default attributes.

        Arguments:
            :id:                `int` Unique 32bit ID value assigned by OCP database
            :confidence:        `float` Value 0-1 indicating confidence in annotation
            :dynamic_metadata:  `dict` A flexible, unspecified collection key-value pairs
            :status:            `string` Status of annotation in database
            :author:            `string` Username of the person who created the annotation
        """
        self._id = id
        self._confidence = confidence
        self._dynamic_metadata = dynamic_metadata
        self._status = status
        self._author = author

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        if type(value) is int:
            return self._id = value
        else:
