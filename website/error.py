from corelib.htmlgen import *
from corelib.phelix import leafComponent


@leafComponent
def Page(exception: Exception):
    return div(
        h1(
            "Error! : ",
            classname="text-5xl text-red-500",
        ),
        p(f"An error occurred: {exception}", classname="text-gray-200 p-4"),
    )
