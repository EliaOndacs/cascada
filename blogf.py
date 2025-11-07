# load the configuration
from src.config import CascadaWebsiteConfig, get_config


config: CascadaWebsiteConfig = get_config()


def render_markdown(markdown: str):
    "render markdown to html"
    from markdown_it import MarkdownIt

    return MarkdownIt().render(markdown)


def get_blog_posts():
    "returns all the blog posts in the following format (name, markdown, is_html) for every blog post"
    for parent, dirs, files in config.blog.walk():
        for file in files:
            if file.endswith(".md"):
                _f = parent / file
                yield (
                    _f.name.removesuffix(".md"),
                    _f.read_text(encoding="utf-8"),
                    False,
                )
            if file.endswith(".html"):
                _f = parent / file
                yield (
                    _f.name.removesuffix(".html"),
                    _f.read_text(encoding="utf-8"),
                    True,
                )
