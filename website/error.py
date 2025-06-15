from corelib.phelix import leafComponent


@leafComponent
def Page(exception: Exception):
    return repr(exception)
