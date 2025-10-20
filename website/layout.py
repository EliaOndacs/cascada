from corelib.htmlgen import *
from corelib.phelix import leafComponent
from src.config import CascadaWebsiteConfig, get_config

config: CascadaWebsiteConfig = get_config()


@leafComponent
def Layout(*children):
    return htmlelement(
        head(
            meta(charset="UTF-8"),
            meta(name="viewport", content="width=device-width, initial-scale=1.0"),
            meta(name="Generator", content="Cascada"),
            link("/public/favicon.png", rel="icon"),
            link("/css/global.css", rel="stylesheet"),
            title(config.name),
        ),
        body(*children),
    )
