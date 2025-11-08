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
            meta(name="theme-color", content="#0a0a0a"),
            link("/public/favicon.png", rel="icon"),
            link("/css/global.output.css", rel="stylesheet"),
            link(
                "https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500&display=swap",
                rel="stylesheet",
            ),
            title(config.name),
        ),
        body(
            *children,
            classname="bg-zinc-900 text-stone-100 antialiased \
                      font-['Inter'] p-6 md:p-10 flex flex-col items-center \
                      leading-relaxed tracking-wide m-4 rounded-3xl \
                      border border-white/5 backdrop-blur-xl \
                      bg-linear-to-b from-zinc-900/80 to-black/80 \
                      shadow-[0_0_45px_-5px_rgba(0,0,0,0.3)]"
        ),
        classname="bg-linear-to-b from-zinc-950 to-black \
                  scroll-smooth selection:bg-red-500/30 selection:text-black",
    )
