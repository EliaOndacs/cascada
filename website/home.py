from corelib.htmlgen import *
from corelib.phelix import leafComponent
from src.config import get_config

config = get_config()


@leafComponent
def Homepage():

    return mainelement(
        img(
            ref="/public/favicon.png",
            alt="Cascada Logo",
            classname="w-24 h-24 mx-auto mb-4 rounded-lg shadow-lg hover:shadow-blue-500/50 transition-all",
        ),
        h1(
            "Welcome to My Website",
            classname="bg-gradient-to-r from-red-500 to-blue-500 text-transparent bg-clip-text transform origin-left transition-all hover:cursor-default hover:translate-x-2 text-shadow shadow-lg text-3xl",
        ),
        p(
            f"""This website is built with Cascada, a modern Python web framework that \
                combines the simplicity of functional components with the power of Python.\
                Cascada offers seamless integration with Tailwind CSS, real-time updates, and a\
                developer-friendly experience for building dynamic web applications. Powered\
                by {a(
                    "corelib",
                    "https://github.com/EliaOndacs/cascada",
                    classname="text-blue-500 hover:text-blue-400 underline transition-colors",
                )}.""",
            classname="text-gray-200 text-sm p-4 bg-gradient-to-r from-blue-900/30 to-red-900/30 rounded-lg shadow-md hover:outline hover:outline-blue-500",
        ),
    )
