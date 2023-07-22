from colorama import Fore

enumval = 0
def enumvalue(reset=False):
    global enumval
    if reset:
        enumval = -1
    enumval += 1
    return enumval


def header(txt: str, width=45, filler='-', align='c'):
    assert align in 'lcr'
    return {'l': txt.ljust, 'c': txt.center, 'r': txt.rjust}[align](width, filler)


def color(color_: Fore, value):
    return f"{color_}{str(value)}{Fore.RESET}"


def auto_str(cls):
    """
    Annotation to auto genereate str for a class.
    Args:
        cls:
    """
    def __str__(self):
        return '%s(%s)' % (
            type(self).__name__,
            ', '.join('%s=%s' % item for item in vars(self).items())
        )

    cls.__str__ = __str__
    return cls
