import asyncio

import asyncpg
import dom_generator as dom
from db import Connection
from dom_generator import material_design as mdc

from . import components


async def _generate():
    conn: asyncpg.Connection
    async with Connection(database="nookdata") as conn:
        data_bugs = await conn.fetch('SELECT * FROM "bugs" ORDER BY "index";')
        data_fish = await conn.fetch('SELECT * FROM "fish" ORDER BY "index";')
    return components.NookDataPage(
        "Critterpedia",
        ["assets/critterpedia.js"],
        "begin_scripts();load_window_if_required();",
        mdc.Card(
            content=dom.ElementGroup(
                dom.ContentDivision(
                    dom.Span("Bugs", class_="critter-type"),
                    dom.Span("0", class_="obtained-count", id="obtained_bugs"),
                    dom.Span("0", class_="modelled-count", id="modelled_bugs"),
                    class_="critter-table-title",
                ),
                dom.Table(
                    *[
                        [
                            components.CritterPanel(
                                bug["name"],
                                bug["normal_name"],
                                bug["index"],
                                bug["quote"],
                                bug["dry"],
                                bug["rain"],
                                bug["price"],
                                bug["location"],
                                [
                                    bug[month]
                                    for month in [
                                        "jan",
                                        "feb",
                                        "mar",
                                        "apr",
                                        "may",
                                        "jun",
                                        "jul",
                                        "aug",
                                        "sep",
                                        "oct",
                                        "nov",
                                        "dec",
                                    ]
                                ],
                                "bugs",
                            )
                            for bug in data_bugs[i::5]
                        ]
                        for i in range(5)
                    ]
                ),
            ),
            class_="padded-container",
            pad=True,
        ),
        mdc.Card(
            content=dom.ElementGroup(
                dom.ContentDivision(
                    dom.Span("Fish", class_="critter-type"),
                    dom.Span("0", class_="obtained-count", id="obtained_fish"),
                    dom.Span("0", class_="modelled-count", id="modelled_fish"),
                    class_="critter-table-title",
                ),
                dom.Table(
                    *[
                        [
                            components.CritterPanel(
                                fish["name"],
                                fish["normal_name"],
                                fish["index"],
                                fish["quote"],
                                fish["dry"],
                                fish["rain"],
                                fish["price"],
                                fish["location"],
                                [
                                    fish[month]
                                    for month in [
                                        "jan",
                                        "feb",
                                        "mar",
                                        "apr",
                                        "may",
                                        "jun",
                                        "jul",
                                        "aug",
                                        "sep",
                                        "oct",
                                        "nov",
                                        "dec",
                                    ]
                                ],
                                "fish",
                                fish["shadow"],
                            )
                            for fish in data_fish[i::5]
                        ]
                        for i in range(5)
                    ]
                ),
            ),
            class_="padded-container",
            pad=True,
        ),
    ).serialise()


def generate():
    return asyncio.run(_generate())


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "w") as file:
        file.write(generate())
