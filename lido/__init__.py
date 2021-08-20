from logging import getLogger, NullHandler

getLogger(__name__).addHandler(NullHandler())
