from tui import components as c

from docs.layouts.root_layout import root_layout


async def docs_layout(children: c.AnyComponents) -> c.AnyComponents:
    layout_children = [
        c.Container(
            tag="main",
            class_name="flex",
            children=[
                c.Container(
                    tag="aside",
                    class_name="py-8 pr-6 flex flex-col gap-6 w-60",
                    children=[
                        c.Container(
                            tag="div",
                            children=[
                                c.Heading(
                                    level=2,
                                    text="Getting Started",
                                    class_name="mb-2",
                                ),
                                c.Container(
                                    tag="nav",
                                    children=[
                                        c.Link(
                                            href="/docs",
                                            children=[
                                                c.Text(
                                                    text="Introduction",
                                                )
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        ),
                        c.Container(
                            tag="div",
                            children=[
                                c.Heading(
                                    level=2,
                                    text="Components",
                                    class_name="mb-2",
                                ),
                                c.Container(
                                    tag="nav",
                                    class_name="flex flex-col gap-2",
                                    children=[
                                        c.Link(
                                            href="/components/avatar",
                                            children=[
                                                c.Text(
                                                    text="Avatar",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/components/button",
                                            children=[
                                                c.Text(
                                                    text="Button",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/components/container",
                                            children=[
                                                c.Text(
                                                    text="Container",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/components/heading",
                                            children=[
                                                c.Text(
                                                    text="Heading",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/components/link",
                                            children=[
                                                c.Text(
                                                    text="Link",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/components/table",
                                            children=[
                                                c.Text(
                                                    text="Table",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/components/text",
                                            children=[
                                                c.Text(
                                                    text="Text",
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                c.Container(tag="section", class_name="py-8 flex-1", children=children),
            ],
        )
    ]
    return await root_layout(layout_children)
