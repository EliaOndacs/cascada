from sanic import Sanic, html

from config import CascadaWebsiteConfig, get_config
from corelib.phelix import Component
from util import getobjfrmfile

# load the configuration
config: CascadaWebsiteConfig = get_config()


# create a sanic application instance
server: Sanic = Sanic(config.name)

# loading the layout component

layout: Component = getobjfrmfile(str(config.layout), "Layout")

# loading homepage and error page before
#  hand so we don't have to do it again
err_page: Component = getobjfrmfile(str(config.error_page), "Page")
hme_page: Component = getobjfrmfile(str(config.homepage), "Homepage")

# registering all the pages and their routes


def register_page(name: str, component: Component):
    "register a toplevel page route"

    @server.get(f"/{route}", name=name)
    async def wrapper(request):
        return html(layout(component()))


for parent, dirs, files in config.pages.walk():
    for file in files:
        if file.endswith(".py"):
            _f = parent / file
            register_page(_f.name, getobjfrmfile(str(_f), "Page"))


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
