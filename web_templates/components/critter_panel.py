import typing

from dom_generator import Component, ElementGroup, IdiomaticText, Image, Script
from dom_generator.material_design import Card, Dialogue

from . import CritterInfo


class CritterPanel(Component):
    def __init__(
        self,
        name: str,
        normal_name: str,
        index: int,
        quote: str,
        dry: bool,
        rain: bool,
        price: int,
        location: str,
        hours: typing.List[typing.List[bool]],
        type: typing.Literal["bugs", "fish"],
        size_or_none: typing.Optional[str] = None,
        # user_owns: typing.Optional[bool] = False,
        # user_owns_model: typing.Optional[bool] = False,
    ) -> None:
        self.content = ElementGroup(
            Card(
                IdiomaticText(
                    "help",  # TODO: make responsive
                    id=f"icon_{type}_{index:0>2}",
                    classes={"material-icons"},
                ),
                Image(
                    src=f"https://starwort.github.io/nookdata/assets/{type}/{index:0>2}.png",
                    # src=f"nookdata/assets/{type}/{index:0>2}.png",
                    style="width:64px; height:64px",
                ),
                onclick=f"open_critter_info('dialogue_{type}_{index:0>2}')",
                title=(
                    f"{name.capitalize()} ({type.capitalize().rstrip('s')} "
                    f"#{index + 1})"
                ),
                pad=False,
                id=f"card_{type}_{index:0>2}",
                outlined=False,
                classes={"critter-panel"},
                **{
                    "data-times": repr(hours).lower(),
                    "data-name": name.lower(),
                    "data-dry": repr(dry).lower(),
                    "data-rain": repr(rain).lower(),
                    "data-price": repr(price),
                    "data-size": repr(size_or_none).replace("'", '"'),
                    "data-location": location.lower(),
                    # "data-caught": repr(user_owns).lower(),
                    # "data-model": repr(user_owns_model).lower(),
                },
            ),
            Dialogue(
                name.capitalize(),
                CritterInfo(
                    normal_name, index, quote, dry, rain, price, location, hours, type
                ),
                id=f"dialogue_{type}_{index:0>2}",
                classes={"critter-info"},
            ),
        )
