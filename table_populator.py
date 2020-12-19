from ast import literal_eval

from db import Connection

with open("availability.csv") as file:
    rows = [literal_eval(line) for line in file.readlines()[1:]]
availability = {"#ROW" + k: [True if i else False for i in v] for k, _, *v in rows}
with open("bugs.csv") as file:
    header, *rows = [literal_eval(line) for line in file.readlines()]
bugs = [{k: v for k, v in zip(header, row)} for row in rows]
with open("fish.csv") as file:
    header, *rows = [literal_eval(line) for line in file.readlines()]
fish = [{k: v for k, v in zip(header, row)} for row in rows]
for bug, fish_ in zip(bugs, fish):
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
    ]:
        bug[month] = availability[bug[month]]
        fish_[month] = availability[fish_[month]]
# print(bugs[0], fish[0])


async def populate_bugs_table():
    async with Connection(database="nookdata") as conn:
        for row in bugs:
            await conn.execute(
                "INSERT INTO bugs(index, dry, rain, name, normal_name, "
                "quote, price, location, jan, feb, mar, apr, may, jun, jul, "
                "aug, sep, oct, nov, dec) VALUES($1, $2, $3, $4, $5, $6, $7, "
                "$8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, "
                "$20)",
                int(row["critterpedia_index"]),
                bool(row["available_dry"]),
                bool(row["available_wet"]),
                row["name"],
                row["normalised_name"],
                row["capture_quote"],
                int(row["price"]),
                row["location"],
                row["jan"],
                row["feb"],
                row["mar"],
                row["apr"],
                row["may"],
                row["jun"],
                row["jul"],
                row["aug"],
                row["sep"],
                row["oct"],
                row["nov"],
                row["dec"],
            )


async def populate_fish_table():
    async with Connection(database="nookdata") as conn:
        for row in fish:
            await conn.execute(
                "INSERT INTO fish(index, dry, rain, name, normal_name, "
                "quote, price, location, jan, feb, mar, apr, may, jun, jul, "
                "aug, sep, oct, nov, dec, shadow) VALUES($1, $2, $3, $4, $5, $6, $7, "
                "$8, $9, $10, $11, $12, $13, $14, $15, $16, $17, $18, $19, "
                "$20, $21)",
                int(row["critterpedia_index"]),
                bool(row["available_dry"]),
                bool(row["available_wet"]),
                row["name"],
                row["normalised_name"],
                row["capture_quote"],
                int(row["price"]),
                row["location"],
                row["jan"],
                row["feb"],
                row["mar"],
                row["apr"],
                row["may"],
                row["jun"],
                row["jul"],
                row["aug"],
                row["sep"],
                row["oct"],
                row["nov"],
                row["dec"],
                {
                    1: "1",
                    2: "2",
                    3: "3",
                    4: "4",
                    5: "5",
                    6: "6",
                    16: "6 (Fin)",
                    26: "6 (Narrow)",
                }[row["size"]],
            )
