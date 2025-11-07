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
                h1(
                    f"#{blog[0]}:",
                    classname="bg-gradient-to-r from-red-500 to-blue-500 text-transparent bg-clip-text transform origin-left transition-all hover:cursor-default  text-shadow shadow-lg text-3xl",
                ),
                div(
                    p(render_markdown(blog[1])) if blog[2] == False else blog[1],
                    classname="bg-zinc-900 text-gray-200 border-gray-700 p-4 rounded-lg shadow-md ",
                ),
                br(),
                classname="bg-zinc-900 text-stone-100 antialiased \
                      font-['Inter'] p-6 md:p-10 flex flex-col items-center \
                      leading-relaxed tracking-wide m-4 rounded-3xl \
                      border border-white/5 backdrop-blur-xl \
                      bg-gradient-to-b from-zinc-900/80 to-black/80 \
                      shadow-[0_0_45px_-5px_rgba(0,0,0,0.3)]",
            )
            for blog in blogs
        )
    )
