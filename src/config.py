from json import load as load_json
import pydantic


class CascadaWebsiteConfig(pydantic.BaseModel):
    name: str
    public: dict[str, pydantic.DirectoryPath]
    error_page: pydantic.FilePath
    homepage: pydantic.FilePath
    layout: pydantic.FilePath
    pages: pydantic.DirectoryPath
    blog: pydantic.DirectoryPath
    subroutes: pydantic.DirectoryPath


def get_config() -> CascadaWebsiteConfig:
    "loads and return the cascada configuration [file at 'cascada.json']"
    with open("cascada.json", "r") as _f:
        return CascadaWebsiteConfig(**load_json(_f))
