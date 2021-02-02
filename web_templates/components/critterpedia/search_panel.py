import dom_generator as dom
from dom_generator import material_design as mdc


class SearchPanel(dom.Component):
    def __init__(self) -> None:
        self.content = mdc.Card(
            "Filter Critters",
            content=dom.ElementGroup(
                mdc.TextField(
                    "Name",
                    "critter-name",
                    oninput="search_parameters.name=this.value;search_critters()",
                ),
                mdc.TextField(
                    "Location",
                    "critter-location",
                    oninput="search_parameters.location=this.value;search_critters()",
                ),
                mdc.TextField(
                    "Size (Fish only)",
                    "critter-size",
                    oninput="search_parameters.size=this.value;search_critters()",
                ),
                mdc.Checkbox(
                    "Available right now",
                    id="critter-now",
                    onchange="search_parameters.available_now_only=this.checked;search_critters()",
                ),
                mdc.Checkbox(
                    "Unavailable from next month",
                    id="critter-soon",
                    onchange="search_parameters.unavailable_soon_only=this.checked;search_critters()",
                ),
                mdc.Checkbox(
                    "Unobtained",
                    id="critter-need",
                    onchange="search_parameters.unobtained_only=this.checked;search_critters()",
                ),
                dom.Span("Price", id="price-label"),
                mdc.Dropdown(
                    "Comparison",
                    [
                        (">=", "is more than", False),
                        ("=", "is exactly", False),
                        ("<=", "is less than", False),
                    ],
                    0,
                    "critter-price-comp",
                    classes={"critter-price-comp"},
                ),
                mdc.TextField(
                    "Value",
                    "critter-price-value",
                    oninput="search_parameters.price=this.value;search_critters()",
                ),
            ),
            classes={"padded-container", "pad-text", "search-container"},
        )
