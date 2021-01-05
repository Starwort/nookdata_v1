import json
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


# def get_widget(type: str, index: int, hours: typing.List[int]):
#     return f"""<canvas class='time-tracker' id="canvas_{type}_{index}" width="1536" height="100">
#     Active hours: <br>
#     00:00 - 00:59: {"Active" if hours[0] else "Inactive"}<br>
#     01:00 - 01:59: {"Active" if hours[1] else "Inactive"}<br>
#     02:00 - 02:59: {"Active" if hours[2] else "Inactive"}<br>
#     03:00 - 03:59: {"Active" if hours[3] else "Inactive"}<br>
#     04:00 - 04:59: {"Active" if hours[4] else "Inactive"}<br>
#     05:00 - 05:59: {"Active" if hours[5] else "Inactive"}<br>
#     06:00 - 06:59: {"Active" if hours[6] else "Inactive"}<br>
#     07:00 - 07:59: {"Active" if hours[7] else "Inactive"}<br>
#     08:00 - 08:59: {"Active" if hours[8] else "Inactive"}<br>
#     09:00 - 09:59: {"Active" if hours[9] else "Inactive"}<br>
#     10:00 - 10:59: {"Active" if hours[10] else "Inactive"}<br>
#     11:00 - 11:59: {"Active" if hours[11] else "Inactive"}<br>
#     12:00 - 12:59: {"Active" if hours[12] else "Inactive"}<br>
#     13:00 - 13:59: {"Active" if hours[13] else "Inactive"}<br>
#     14:00 - 14:59: {"Active" if hours[14] else "Inactive"}<br>
#     15:00 - 15:59: {"Active" if hours[15] else "Inactive"}<br>
#     16:00 - 16:59: {"Active" if hours[16] else "Inactive"}<br>
#     17:00 - 17:59: {"Active" if hours[17] else "Inactive"}<br>
#     18:00 - 18:59: {"Active" if hours[18] else "Inactive"}<br>
#     19:00 - 19:59: {"Active" if hours[19] else "Inactive"}<br>
#     20:00 - 20:59: {"Active" if hours[20] else "Inactive"}<br>
#     21:00 - 21:59: {"Active" if hours[21] else "Inactive"}<br>
#     22:00 - 22:59: {"Active" if hours[22] else "Inactive"}<br>
#     23:00 - 23:59: {"Active" if hours[23] else "Inactive"}
# </canvas>
# <script>
#     var canvas_{type}_{index} = document.getElementById('canvas_{type}_{index}');
#     var ctx_{type}_{index} = canvas_{type}_{index}.getContext('2d');
#     var avail_hours_{type}_{index} = {hours!r};
#     var hour_width_{type}_{index} = canvas_{type}_{index}.width / 24;
#     var debug_{type}_{index} = false;
#     function draw_{type}_{index}() {{
#         ctx_{type}_{index}.clearRect(0, 0, canvas_{type}_{index}.width, canvas_{type}_{index}.height);
#         //console.log(avail_hours);
#         ctx_{type}_{index}.fillStyle = "#ffff007f";
#         for (var i = 0; i < 24; i++) {{
#             if (avail_hours_{type}_{index}[i]) {{
#                 if (debug)
#                     console.log(`[TIMES] hour ${{i}} active at ${{i * hour_width_{type}_{index}}}`);
#                 ctx_{type}_{index}.fillRect(i * hour_width_{type}_{index}, canvas_{type}_{index}.height / 4, hour_width_{type}_{index}, canvas_{type}_{index}.height / 2);
#             }} else {{
#                 if (debug)
#                     console.log(`[TIMES] hour ${{i}} inactive at ${{i * hour_width_{type}_{index}}}`);
#             }}
#         }}
#         ctx_{type}_{index}.strokeStyle = "#ffffff7f";
#         //ctx.lineWidth = 2;
#         ctx_{type}_{index}.beginPath();
#         for (var i = 0; i <= 24; i++) {{
#             if (i % 12 == 0) {{
#                 if (debug)
#                     console.log(`[LINES] big line ${{i}} at ${{i * hour_width}}`);
#                 ctx_{type}_{index}.moveTo(i * hour_width_{type}_{index}, 0);
#                 ctx_{type}_{index}.lineTo(i * hour_width_{type}_{index}, canvas_{type}_{index}.height);
#             }} else if (i % 6 == 0) {{
#                 if (debug)
#                     console.log(`[LINES] med line ${{i}} at ${{i * hour_width_{type}_{index}}}`);
#                 ctx_{type}_{index}.moveTo(i * hour_width_{type}_{index}, canvas_{type}_{index}.height / 8);
#                 ctx_{type}_{index}.lineTo(i * hour_width_{type}_{index}, canvas_{type}_{index}.height * 7 / 8);
#             }} else {{
#                 if (debug)
#                     console.log(`[LINES] sml line ${{i}} at ${{i * hour_width_{type}_{index}}}`);
#                 ctx_{type}_{index}.moveTo(i * hour_width_{type}_{index}, canvas_{type}_{index}.height / 4);
#                 ctx_{type}_{index}.lineTo(i * hour_width_{type}_{index}, canvas_{type}_{index}.height * 3 / 4);
#             }}
#         }}
#         ctx_{type}_{index}.stroke();
#         ctx_{type}_{index}.strokeStyle = '#ff0000';
#         ctx_{type}_{index}.beginPath();
#         var today = new Date();
#         var x = canvas_{type}_{index}.width * (today.getHours() * 3600 + today.getMinutes() * 60 + today.getSeconds()) / 86400;
#         if (debug)
#             console.log(`[CTIME] x = ${{canvas_{type}_{index}.width}} * (${{today.getHours()}} * 3600 + ${{today.getMinutes()}} * 60 + ${{today.getSeconds()}}) / 86400 = ${{x}}`);
#         ctx_{type}_{index}.moveTo(x, 0);
#         ctx_{type}_{index}.lineTo(x, canvas.height);
#         ctx_{type}_{index}.stroke();
#     }}
#     window.setTimeout(draw_{type}_{index}, 0);
#     window.setInterval(draw_{type}_{index}, 500);
# </script>"""
