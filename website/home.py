from corelib.htmlgen import *
from corelib.phelix import leafComponent
from src.config import get_config

config = get_config()


@leafComponent
def Homepage():
    return mainelement(
        div(
            img(ref="/public/favicon.png", classname="logo"),
            h1(f"Welcome to {config.name.title()}!"),
        ),
        div("Powered By ", a("Cascada", "https://github.com/EliaOndacs/cascada")),
    )
