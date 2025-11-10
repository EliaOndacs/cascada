import subprocess
import time
from sanic import Blueprint, Sanic, html


from corelib.phelix import Component
from src.config import CascadaWebsiteConfig, get_config
from src.util import getobjfrmfile
from blogf import get_blog_posts, render_markdown


# load the configuration
config: CascadaWebsiteConfig = get_config()


# create a sanic application instance
server: Sanic = Sanic(config.name.replace(" ", "-").capitalize())
blog = Blueprint("blog", "/blog")

# loading the layout component

layout: Component = getobjfrmfile(str(config.layout), "Layout")

# loading homepage and error page before
#  hand so we don't have to do it again
err_page: Component = getobjfrmfile(str(config.error_page), "Page")
hme_page: Component = getobjfrmfile(str(config.homepage), "Homepage")

# all the register functions


def register_page(name: str, component: Component):
    "register a toplevel page route"

    @server.get(f"/{name}", name=name)
    async def wrapper(request):
        return html(layout(component()))


def register_page_from_view(
    name: str, view: str, *, blueprint: Blueprint | None = None
):
    "register a toplevel page route using a direct view"

    if blueprint:
        decorator = blueprint.get(f"/{name}", name=name)
    else:
        decorator = server.get(f"/{name}", name=name)

    @decorator
    async def wrapper(request):
        return html(layout(view))


def register_subroute(parent: str, name: str, component: Component):
    "register a subroute for a page"

    @server.get(f"/{parent}/{name}", name=name)
    async def wrapper(request):
        return html(layout(component()))


def register_subroute_from_view(parent: str, name: str, view: str):
    "register a subroute for a page using a direct view"

    @server.get(f"/{parent}/{name}", name=name)
    async def wrapper(request):
        return html(layout(view))


# registering all the pages and their routes


for parent, dirs, files in config.pages.walk():
    for file in files:
        if file.endswith(".py"):
            _f = parent / file
            register_page(_f.name.removesuffix(".py"), getobjfrmfile(str(_f), "Page"))
        if file.endswith(".md"):
            _f = parent / file
            register_page_from_view(
                _f.name.removesuffix(".md"),
                render_markdown(_f.read_text(encoding="utf-8")),
            )
        if file.endswith(".html"):
            _f = parent / file
            register_page_from_view(
                _f.name.removesuffix(".html"),
                render_markdown(_f.read_text(encoding="utf-8")),
            )


# register all the subroutes and their pages


for parent, dirs, _ in config.subroutes.walk():
    for _dir in dirs:
        for parent2, _, files in (parent / _dir).walk():
            for file in files:
                if file.endswith(".py"):
                    _f = parent2 / file
                    register_subroute(
                        _dir,
                        _f.name.removesuffix(".py"),
                        getobjfrmfile(str(_f), "Page"),
                    )
                if file.endswith(".md"):
                    _f = parent / file
                    register_subroute_from_view(
                        _dir,
                        _f.name.removesuffix(".md"),
                        render_markdown(_f.read_text(encoding="utf-8")),
                    )
                if file.endswith(".html"):
                    _f = parent / file
                    register_subroute_from_view(
                        _dir,
                        _f.name.removesuffix(".html"),
                        _f.read_text(encoding="utf-8"),
                    )


# compiling all the css using tailwind

css_path = config.public.get("css", None)


if css_path:
    for parent, dirs, files in css_path.walk():
        for file in files:
            if file.endswith(".output.css"):
                (parent / file).unlink(True)

    for parent, dirs, files in css_path.walk():
        for file in files:
            if file.endswith(".output.css") or not file.endswith(".css"):
                continue

            inp, out = parent / file, parent / (
                file.removesuffix(".css") + ".output.css"
            )

            command = f"tailwindcss -m -i {str(inp).replace("\\", "/")} -o {str(out).replace("\\", "/")}"
            result = subprocess.run(command, shell=True)
            result.check_returncode()
            time.sleep(0.1)

            if not out.exists():
                raise RuntimeError(f"Tailwind did not produce {str(out)!r}")

# loading and rendering the blog pages


for post in get_blog_posts():
    register_page_from_view(post[0], render_markdown(post[1]), blueprint=blog)

server.blueprint(blog)


# setting up the custom error pages
@server.exception(Exception)
async def error_page(request, exception):
    return html(layout(err_page(exception)))


# setting up the homepage
@server.get("/")
async def homepage(request):
    return html(layout(hme_page()))


# loading all the public directories that are meant to be served
for route in config.public:
    path = config.public[route]
    server.static(
        uri=f"/{route}", file_or_directory=str(path), name=route, resource_type="dir"
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(server)
# end main
