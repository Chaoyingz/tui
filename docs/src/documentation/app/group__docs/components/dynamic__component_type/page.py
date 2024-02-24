from typing import Annotated, Any, Literal, Optional

import tui.components as c
from fastapi import Path
from pydantic import BaseModel, Field
from pydantic_core._pydantic_core import PydanticUndefined
from tui import Meta, PageResponse
from tui.form import Checkbox, Input, Select, Textarea
from tui.sitemap import Sitemap


def get_component_description_section(
    title: str,
    description: str,
) -> c.Container:
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=1,
                text=title,
                class_name="text-3xl mb-3",
            ),
            c.Text(text=description),
        ],
    )


class ComponentProps(BaseModel):
    prop: str
    type: str
    default: Optional[str]
    description: Optional[str]


def get_component_preview_literal_component(
    component_type: c.AnyComponent,
    literal_props: list[str],
    dynamic_props: list[str],
    default_props_values: dict[str, Any],
) -> c.Container:
    return c.Container(
        tag="div",
        class_name="flex flex-col gap-10",
        children=[
            c.Container(
                tag="div",
                children=[
                    c.Heading(
                        level=3,
                        text=literal_prop,
                    ),
                    c.Container(
                        tag="div",
                        class_name="flex gap-4 mt-3",
                        children=[
                            component_type(
                                **{
                                    literal_prop: literal_value,
                                    **{dp: literal_value for dp in dynamic_props},
                                    **default_props_values,
                                }
                            )
                            for literal_value in component_type.__annotations__[literal_prop].__args__
                        ],
                    ),
                ],
            )
            for literal_prop in literal_props
        ],
    )


def get_component_preview_section(
    preview: c.AnyComponent,
) -> c.AnyComponent:
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=2,
                text="Preview",
                class_name="text-2xl mb-6 border-b pb-2",
            ),
            preview,
        ],
    )


def get_component_api_reference_section(component: c.AnyComponent) -> c.Container:
    props = []
    for field, filed_info in component.model_fields.items():
        if field == "component_type":
            continue
        if field == "children":
            filed_info.annotation = "tui.components.AnyComponents"
            filed_info.default = "[]"
            filed_info.description = "The children of the component."
        if filed_info.default == PydanticUndefined:
            filed_info.default = "-"
        props.append(
            ComponentProps(
                prop=field,
                type=str(filed_info.annotation),
                default=filed_info.default or "-",
                description=filed_info.description,
            )
        )
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=2,
                text="API Reference",
                class_name="text-2xl mb-6 border-b pb-2",
            ),
            c.Table(datasets=props),
        ],
    )


def get_component_page(
    description_section: c.AnyComponent,
    preview_section: c.AnyComponent,
    api_reference_section: c.AnyComponent,
) -> c.AnyComponent:
    return c.Container(
        tag="div",
        class_name="flex gap-12 flex-col",
        children=[description_section, preview_section, api_reference_section],
    )


class TableExampleModel(BaseModel):
    column1: str
    column2: str
    column3: str


class FormExampleModel(BaseModel):
    username: Annotated[str, Input(placeholder="Enter your username")] = Field(
        pattern=r"^[a-zA-Z0-9]+$", min_items=2, max_items=10
    )
    gender: Annotated[Literal["male", "female"], Select()] = Field(
        default="male", description="The gender of the user."
    )
    password: Annotated[str, Input(type="password", placeholder="Enter your password")]
    hobby: Annotated[Optional[str], Textarea(placeholder="Type your hobby")] = Field(
        None, description="The hobby of the user."
    )
    terms_accepted: Annotated[bool, Checkbox(class_name="ml-3")] = Field(
        default=False, description="The terms accepted by the user."
    )


COMPONENT_DOCS_MAP = {
    "avatar": get_component_page(
        description_section=get_component_description_section(
            title="Avatar",
            description="An avatar is a visual representation of a user or a group of users.",
        ),
        preview_section=get_component_preview_section(
            preview=c.Container(
                tag="div",
                class_name="flex gap-3",
                children=[
                    c.Avatar(
                        src="https://github.com/shadcn.png",
                        alt="@shadcn",
                        fallback="CN",
                    ),
                    c.Avatar(
                        fallback="CN",
                    ),
                ],
            )
        ),
        api_reference_section=get_component_api_reference_section(component=c.Avatar),
    ),
    "button": get_component_page(
        description_section=get_component_description_section(
            title="Button",
            description="A control that triggers an action. Button labels should express what action will occur when the ",
        ),
        preview_section=get_component_preview_section(
            preview=get_component_preview_literal_component(
                component_type=c.Button,
                literal_props=["variant", "size"],
                dynamic_props=["children"],
                default_props_values={},
            )
        ),
        api_reference_section=get_component_api_reference_section(component=c.Button),
    ),
    "container": get_component_page(
        description_section=get_component_description_section(
            title="Container",
            description="A container component.",
        ),
        preview_section=c.Container(
            tag="div",
        ),
        api_reference_section=get_component_api_reference_section(component=c.Container),
    ),
    "form": get_component_page(
        description_section=get_component_description_section(
            title="Form",
            description="A form component serves as a container for collecting user inputs through various form "
            "elements like input fields, checkboxes, radio buttons, and dropdowns. ",
        ),
        preview_section=get_component_preview_section(
            preview=c.Form(model=FormExampleModel, submit_url="/components/form/"),
        ),
        api_reference_section=get_component_api_reference_section(component=c.Form),
    ),
    "heading": get_component_page(
        description_section=get_component_description_section(
            title="Heading",
            description="A heading component.",
        ),
        preview_section=get_component_preview_section(
            preview=c.Heading(
                level=2,
                text="Heading",
            )
        ),
        api_reference_section=get_component_api_reference_section(component=c.Heading),
    ),
    "link": get_component_page(
        description_section=get_component_description_section(
            title="Link",
            description="A link component.",
        ),
        preview_section=get_component_preview_section(
            preview=c.Link(
                href="/",
                children=[
                    c.Text(
                        text="Link",
                    )
                ],
            )
        ),
        api_reference_section=get_component_api_reference_section(component=c.Link),
    ),
    "table": get_component_page(
        description_section=get_component_description_section(
            title="Table",
            description="A table component is used to display data in a structured, grid-like format consisting of rows"
            " and columns.",
        ),
        preview_section=get_component_preview_section(
            preview=c.Table(
                datasets=[
                    TableExampleModel(
                        column1="Value 1",
                        column2="Value 2",
                        column3="Value 3",
                    ),
                    TableExampleModel(
                        column1="Value 4",
                        column2="Value 5",
                        column3="Value 6",
                    ),
                ]
            )
        ),
        api_reference_section=get_component_api_reference_section(component=c.Table),
    ),
    "text": get_component_page(
        description_section=get_component_description_section(
            title="Text",
            description="A text component.",
        ),
        preview_section=get_component_preview_section(
            preview=c.Text(
                text="Text",
            )
        ),
        api_reference_section=get_component_api_reference_section(component=c.Text),
    ),
}


async def sitemap(dynamic_url: str) -> list[Sitemap]:
    return [
        Sitemap(
            url=dynamic_url.format(component_type=component_type),
            last_modified=None,
            change_frequency=None,
            priority=None,
        )
        for component_type in COMPONENT_DOCS_MAP
    ]


async def page(
    component_type: Annotated[str, Path(..., description="The component type to render")],
) -> PageResponse:
    return PageResponse(
        meta=Meta(
            title=f"{component_type} component",
            description=f"{component_type} component",
        ),
        element=COMPONENT_DOCS_MAP.get(component_type, c.Text(text="Component Not found")),
    )
