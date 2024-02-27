from starlette.concurrency import run_in_threadpool
from tui import PageResponse
from tui import components as c

from documentation.utils import get_markdown_content


async def page() -> PageResponse:
    readme_text = await run_in_threadpool(get_markdown_content, "introduction.md")
    return PageResponse(
        element=c.Container(
            tag="div",
            children=[
                c.Markdown(
                    text=readme_text,
                ),
                c.Container(
                    tag="div",
                    class_name="mt-10 flex justify-end",
                    children=[
                        c.Link(
                            href="/docs/installation/",
                            children=[c.Button(children="Installation >", variant="outline", size="sm")],
                        )
                    ],
                ),
            ],
        )
    )