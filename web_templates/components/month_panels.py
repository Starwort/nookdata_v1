import typing

from dom_generator import Component, ElementGroup, Script, Table
from dom_generator.material_design import Card


def chunk(data, n: int):
    return zip(*([iter(data)] * n))


class MonthPanels(Component):
    __slots__ = ()

    def __init__(self, hours: typing.List[typing.List[bool]], identifier: str) -> None:
        self.content = ElementGroup(
            Table(
                *chunk(
                    [
                        Card(
                            content=month,
                            classes=(
                                {
                                    "card-" + season,
                                    ("card-inactive" if not any(times) else ""),
                                }
                                - {""}
                            ),
                            id=f"card_{i}_{identifier}",
                            outlined=True,
                        )
                        for i, (month, season, times) in enumerate(
                            zip(
                                [
                                    "January",
                                    "February",
                                    "March",
                                    "April",
                                    "May",
                                    "June",
                                    "July",
                                    "August",
                                    "September",
                                    "October",
                                    "November",
                                    "December",
                                ],
                                [
                                    "winter",
                                    "winter",
                                    "spring",
                                    "spring",
                                    "spring",
                                    "summer",
                                    "summer",
                                    "summer",
                                    "autumn",
                                    "autumn",
                                    "autumn",
                                    "winter",
                                ],
                                hours,
                            )
                        )
                    ],
                    3,
                ),
                classes={"month-panels"},
            ),
            Script(f"add_card_set({identifier!r});"),
        )
