import asyncio

import asyncpg
import dom_generator as dom
from db import Connection
from dom_generator import material_design as mdc

from . import components


async def _generate():
    conn: asyncpg.Connection
    async with Connection(database="nookdata") as conn:
        bugs = await conn.fetch('SELECT * FROM "bugs" ORDER BY "index";')
        fishes = await conn.fetch('SELECT * FROM "fish" ORDER BY "index";')
    return dom.HTML(
        dom.Head(
            mdc.MaterialDesignInitialiser(),
            dom.Title("Critterpedia | Nookdata"),
            dom.Link(rel="stylesheet", href="assets/nookdata.css"),
            dom.Script("", src="assets/critterpedia.js"),
        ),
        dom.Body(
            mdc.AppBar("NookData", mdc.ThemeSwitcherButton()),
            dom.MainContent(
                mdc.Card(
                    content=dom.Table(
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
                                for bug in bugs[i::5]
                            ]
                            for i in range(5)
                        ]
                    ),
                    class_="padded-container",
                    pad=True,
                ),
                mdc.Card(
                    content=dom.Table(
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
                                )
                                for fish in fishes[i::5]
                            ]
                            for i in range(5)
                        ]
                    ),
                    class_="padded-container",
                    pad=True,
                ),
            ),
            mdc.MaterialDesignFinaliser(),
            dom.Script("begin_scripts();load_window_if_required();"),
        ),
    ).serialise()


def generate():
    return asyncio.run(_generate())


if __name__ == "__main__":
    import sys

    with open(sys.argv[1], "w") as file:
        file.write(generate())
