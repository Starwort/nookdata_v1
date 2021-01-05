import typing

from dom_generator import Anchor, Component, ElementGroup, LineBreak, Table

from .info_panel import InfoPanel
from .month_panels import MonthPanels
from .time_tracker import TimeTracker


class CritterInfo(Component):
    __slots__ = ()

    def __init__(
        self,
        normal_name: str,
        index: int,
        quote: str,
        dry: bool,
        rain: bool,
        price: int,
        location: str,
        hours: list[list[bool]],
        type: typing.Literal["bugs", "fish"],
        size_if_fish: typing.Optional[str] = None,
    ) -> None:
        self.content = Table(
            [
                Anchor(
                    "arrow_back" if index else "_",
                    classes={
                        "material-icons",
                        ("cursor-pointer" if index else "cursor-default"),
                    },
                    onclick=(
                        f"switch_critter('dialogue_{type}_{index - 1:0>2}')"
                        if index
                        else ""
                    ),
                ),
                ElementGroup(
                    f"{type.capitalize().rstrip('s')} #{index + 1}",
                    LineBreak(),
                    quote,
                    MonthPanels(hours, f"{type}_{index:0>2}"),
                    TimeTracker(f"{type}_{index:0>2}", hours),
                    InfoPanel(index, dry, rain, price, location, type, size_if_fish),
                ),
                Anchor(
                    "arrow_forward" if index < 79 else "_",
                    classes={
                        "material-icons",
                        ("cursor-pointer" if index < 79 else "cursor-default"),
                    },
                    onclick=(
                        f"switch_critter('dialogue_{type}_{index + 1:0>2}')"
                        if index < 79
                        else ""
                    ),
                ),
            ]
        )
