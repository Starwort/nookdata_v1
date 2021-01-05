import typing

import dom_generator as dom
import dom_generator.material_design as mdc


class InfoPanel(dom.Component):
    __slots__ = ()

    def __init__(
        self,
        index: int,
        dry: bool,
        rain: bool,
        price: int,
        location: str,
        type: typing.Literal["bugs", "fish"],
    ) -> None:
        self.content = mdc.Card(
            content=dom.ElementGroup(
                dom.Image(
                    src=f"assets/{type}/{index:0>2}.png",
                ),
            ),
            outlined=True,
            classes={"info-panel"},
        )
