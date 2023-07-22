from dsl.implemented.utility.util import auto_str


@auto_str
class Argument:
    """
    Represents commonly used arguments for selenium web driver methods.
    If the maximum wait time is not specified in the Argument object, it is set to 0.

    """

    def __init__(self, element_name=None, selector=None, negate=False, filename=None, value=None, timeout=0,
                 dictionary=None):
        self.element_name = element_name
        self.selector = selector
        self.negate = negate
        self.filename = filename
        self.timeout = timeout
        self.value = value
        self.dictionary = dictionary
