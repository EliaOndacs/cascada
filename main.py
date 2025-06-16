from sanic import Blueprint, Sanic, html


from corelib.phelix import Component
from src.config import CascadaWebsiteConfig, get_config
from src.util import getobjfrmfile

# make sure default database is created
import db

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

# registering all the pages and their routes


def register_page(name: str, component: Component):
    "register a toplevel page route"

    @server.get(f"/{name}", name=name)
    async def wrapper(request):
        return html(layout(component()))


for parent, dirs, files in config.pages.walk():
    for file in files:
        if file.endswith(".py"):
            _f = parent / file
            register_page(_f.name.removesuffix(".py"), getobjfrmfile(str(_f), "Page"))

# register all the subroutes and their pages


def register_subroute(parent: str, name: str, component: Component):
    "register a subroute for a page"

    @server.get(f"/{parent}/{name}", name=name)
    async def wrapper(request):
        return html(layout(component()))


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

# loading and rendering the blog pages


def register_blog_page(name: str, content: str):
    "register a blog page"

    @blog.get(f"/{name}", name=name)
    async def wrapper(request):
        return html(layout(content))


def render_markdown(markdown: str):
    "render markdown to html"
    from markdown_it import MarkdownIt

    return MarkdownIt().render(markdown)


for parent, dirs, files in config.blog.walk():
    for file in files:
        if file.endswith(".md"):
            _f = parent / file
            register_blog_page(
                _f.name.removesuffix(".md"), render_markdown(_f.read_text())
            )

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
