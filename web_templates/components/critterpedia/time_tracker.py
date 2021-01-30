import typing

import dom_generator as dom


class TimeTracker(dom.Component):
    __slots__ = ()

    def __init__(self, identifier: str, hours: typing.List[typing.List[bool]]):
        self.content = dom.ElementGroup(
            dom.Canvas(
                # "Active Hours:",
                # dom.Table(
                #     [
                #         "Month",
                #         "00:00 - 00:59",
                #         "01:00 - 01:59",
                #         "02:00 - 02:59",
                #         "03:00 - 03:59",
                #         "04:00 - 04:59",
                #         "05:00 - 05:59",
                #         "06:00 - 06:59",
                #         "07:00 - 07:59",
                #         "08:00 - 08:59",
                #         "09:00 - 09:59",
                #         "10:00 - 10:59",
                #         "11:00 - 11:59",
                #         "12:00 - 12:59",
                #         "13:00 - 13:59",
                #         "14:00 - 14:59",
                #         "15:00 - 15:59",
                #         "16:00 - 16:59",
                #         "17:00 - 17:59",
                #         "18:00 - 18:59",
                #         "19:00 - 19:59",
                #         "20:00 - 20:59",
                #         "21:00 - 21:59",
                #         "22:00 - 22:59",
                #         "23:00 - 23:59",
                #     ],
                #     *[
                #         [
                #             [
                #                 "January",
                #                 "February",
                #                 "March",
                #                 "April",
                #                 "May",
                #                 "June",
                #                 "July",
                #                 "August",
                #                 "September",
                #                 "October",
                #                 "November",
                #                 "December",
                #             ][month],
                #             *[
                #                 dom.Checkbox(checked=hour, disabled=True)
                #                 for hour in times
                #             ],
                #         ]
                #         for month, times in enumerate(hours)
                #     ],
                # ),
                width=3360,
                height=140,
                classes={"time-tracker"},
                id="time_tracker_canvas_" + identifier,
            ),
            dom.Script(
                f"add_time_tracker('time_tracker_canvas_{identifier}',"
                f"JSON.parse(document.getElementById('card_{identifier}')"
                ".getAttribute('data-times')))"
            ),
        )
