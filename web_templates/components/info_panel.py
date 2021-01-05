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
        size_if_fish: typing.Optional[str] = None,
    ) -> None:
        self.content = mdc.Card(
            content=dom.ElementGroup(
                dom.Image(
                    src=f"assets/{type}/{index:0>2}.png",
                ),
                (
                    dom.IdiomaticText(
                        "wb_sunny",
                        classes={"material-icons", "dry-indicator"},
                        title="Available when not raining",
                    )
                    if dry
                    else ""
                ),
                (
                    dom.IdiomaticText(
                        "wb_cloud",
                        classes={"material-icons", "rain-indicator"},
                        title="Available when raining",
                    )
                    if rain
                    else ""
                ),
                dom.Paragraph("Found:", classes={"label-location"}),
                dom.Paragraph(location, classes={"location"}),
                dom.Paragraph("Sells for:", classes={"label-sell-value"}),
                dom.Paragraph(str(price), classes={"sell-value"}),
                (
                    dom.Paragraph("Shadow size:", classes={"label-shadow-size"})
                    if type == "fish"
                    else ""
                ),
                (
                    dom.Paragraph(size_if_fish, classes={"shadow-size"})
                    if type == "fish"
                    else ""
                ),
            ),
            outlined=True,
            classes={"info-panel"},
        )
