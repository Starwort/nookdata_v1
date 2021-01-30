import dom_generator as dom
import dom_generator.material_design as mdc

NAVIGATION_ITEMS = [
    mdc.NavigationItem("emoji_nature", "critterpedia.html", "Critterpedia"),
]


class NookDataPage(dom.Component):
    __slots__ = ()

    def __init__(
        self,
        page_title: str,
        included_scripts: list[str],
        trailing_script: str,
        *content: dom.ElementOrText,
    ) -> None:
        for nav_item in NAVIGATION_ITEMS:
            if nav_item.page_title == page_title:
                nav_item.activate()
        self.content = dom.HTML(
            dom.Head(
                mdc.MaterialDesignInitialiser("assets"),
                dom.Title(f"{page_title} | NookData"),
                dom.Link(rel="stylesheet", href="assets/nookdata.css"),
                dom.Script(src="assets/nookdata.js"),
                *[dom.Script(src=script) for script in included_scripts],
            ),
            dom.Body(
                mdc.AppBar("NookData", mdc.ThemeSwitcherButton()),
                mdc.NavigationDrawer(NAVIGATION_ITEMS),
                mdc.AppContent(
                    dom.MainContent(
                        dom.ContentDivision(*content, classes={"main-content"})
                    ),
                ),
                mdc.MaterialDesignFinaliser("assets"),
                dom.Script(trailing_script) if trailing_script else "",
                theme="dark",
            ),
        )
