
def prepend_base(cls,base):
    cls.__bases__ = (base,)+cls.__bases__
    return cls.__bases__

