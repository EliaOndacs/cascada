from corelib.htmlgen import *
from corelib.phelix import leafComponent
from blogf import render_markdown, get_blog_posts


@leafComponent
def Page():
    blogs = list(get_blog_posts())
    if len(blogs) == 0:
        return mainelement(span("No Blog Post Found"))
    return mainelement(
        *(
            div(
                h1(blog[0]),
                div(render_markdown(blog[1])) if blogs[2] == False else blog[1],
                br(),
            )
            for blog in blogs
        )
    )
