from tui import components as c


async def site_header() -> c.AnyComponent:
    return c.Container(
        tag="header",
        class_name="flex w-full justify-between container h-14 border-b items-center text-sm",
        children=[
            c.Container(
                tag="nav",
                class_name="flex items-center gap-6",
                children=[
                    c.Link(
                        href="/",
                        children=[
                            c.Text(
                                text="tui",
                                class_name="font-medium text-xl",
                            )
                        ],
                    ),
                    c.Link(
                        href="/docs",
                        children=[
                            c.Text(
                                text="Docs",
                            )
                        ],
                    ),
                    c.Link(
                        href="/components",
                        children=[
                            c.Text(
                                text="Components",
                            )
                        ],
                    ),
                ],
            ),
            c.Container(
                tag="div",
                children=[
                    c.Link(
                        href="https://github.com/Chaoyingz/tui",
                        children=[
                            c.Text(
                                text="GitHub",
                            )
                        ],
                    )
                ],
            ),
        ],
    )
