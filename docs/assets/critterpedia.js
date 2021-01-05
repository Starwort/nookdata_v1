var canvases = {};
/** @type {String[]} */
var card_sets = [];
var now = new Date();
var hour = now.getHours();
var minute = now.getMinutes();
var second = now.getSeconds();
var month = (now.getMonth() + 11) % 12;
function add_time_tracker(canvas_id, hours) {
    canvases[canvas_id] = hours;
}
function add_card_set(card_set_id) {
    card_sets.push(card_set_id);
}
window.add_time_tracker = add_time_tracker;
window.add_card_set = add_card_set;

function update() {
    now = new Date();
    let old_hour = hour;
    hour = now.getHours();
    minute = now.getMinutes();
    second = now.getSeconds();
    var new_month = now.getMonth();
    var line_colour = window.getComputedStyle(document.querySelector("body"))
        .getPropertyValue("--mdc-theme-on-surface")
        .trim();
    var shorthand_regex = /(?<=^#?)([a-f\d])([a-f\d])([a-f\d])$/i;
    line_colour = line_colour.replace(shorthand_regex, function (m, r, g, b) {
        return r + r + g + g + b + b;
    });
    // console.log(line_colour);
    for (let [canvas_id, hours] of Object.entries(canvases)) {
        draw(canvas_id, hours, line_colour);
    }
    if (new_month != month) {
        for (let card_id of card_sets) {
            // f"card_{i}_{identifier}"
            document.getElementById(`card_${month}_${card_id}`)
                .classList.remove("card-current");
            document.getElementById(`card_${new_month}_${card_id}`)
                .classList.add("card-current");
        }
        month = new_month;
    }
    if (old_hour != hour) {
        if (search_parameters.available_now_only) {
            search_critters();
        }
    }
}

window.time_tracker_width = 6;
function draw(canvas_id, canvas_hours, line_colour) {
    var canvas = document.getElementById(canvas_id);
    var ctx = canvas.getContext("2d");
    var avail_hours = canvas_hours[now.getMonth()];
    var hour_width = canvas.width / 24;
    var debug = false;
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    // console.log(avail_hours);
    ctx.fillStyle = "#ffff007f";
    for (var i = 0; i < 24; i++) {
        if (avail_hours[i]) {
            if (debug)
                console.log(`[TIMES] hour ${i} active at ${i * hour_width}`);
            ctx.fillRect(
                i * hour_width, canvas.height / 4, hour_width, canvas.height / 2);
        } else {
            if (debug)
                console.log(`[TIMES] hour ${i} inactive at ${i * hour_width}`);
        }
    }
    ctx.strokeStyle = line_colour + "7f";
    // ctx.lineWidth = 2;
    ctx.beginPath();
    for (var i = 0; i <= 24; i++) {
        if (i % 12 == 0) {
            if (debug)
                console.log(`[LINES] big line ${i} at ${i * hour_width}`);
            ctx.lineWidth = window.time_tracker_width * 2;
            ctx.moveTo(i * hour_width, 0);
            ctx.lineTo(i * hour_width, canvas.height);
        } else if (i % 6 == 0) {
            if (debug)
                console.log(`[LINES] med line ${i} at ${i * hour_width}`);
            ctx.lineWidth = window.time_tracker_width * 1.5;
            ctx.moveTo(i * hour_width, canvas.height / 8);
            ctx.lineTo(i * hour_width, canvas.height * 7 / 8);
        } else {
            if (debug)
                console.log(`[LINES] sml line ${i} at ${i * hour_width}`);
            ctx.lineWidth = window.time_tracker_width;
            ctx.moveTo(i * hour_width, canvas.height / 4);
            ctx.lineTo(i * hour_width, canvas.height * 3 / 4);
        }
    }
    ctx.stroke();
    ctx.strokeStyle = "#ff0000";
    ctx.beginPath();
    var x = canvas.width * (hour * 3600 + minute * 60 + second) / 86400;
    ctx.lineWidth = window.time_tracker_width;
    if (debug)
        console.log(`[CTIME] x = ${canvas.width} * (${hour} * 3600 + ${minute} * 60 + ${second}) / 86400 = ${x}`);
    ctx.moveTo(x, 0);
    ctx.lineTo(x, canvas.height);
    ctx.stroke();
}
function load_or_unload_dialogue(dialogue, push = true) {
    if (dialogue !== null) {
        window.active_critter_info = dialogue;
        var url = new URL(window.location.href);
        [_, type, index] = dialogue.split("_");
        if (url.searchParams.get("type") === null) {
            url.searchParams.append("type", type.replace("bugs", "bug"));
        }
        if (url.searchParams.get("index") === null) {
            url.searchParams.append("index", Number(index));
        }
        var dialogue_elem = document.getElementById(dialogue);
        var critter_name = dialogue_elem.querySelector(".mdc-dialog__title").innerText;
        if (push) {
            window.history.pushState(
                dialogue, "Critterpedia - " + critter_name + " | Nookdata", url.href);
        } else {
            window.history.replaceState(
                dialogue, "Critterpedia - " + critter_name + " | Nookdata", url.href);
        }
        document.title = "Critterpedia - " + critter_name + " | Nookdata";
        window.setTimeout(window.open_dialogue, 0, dialogue);
    } else {
        if (window.active_critter_info !== null) {
            window.close_dialogue(window.active_critter_info);
        }
        window.active_critter_info = null;
        var url = new URL(window.location.href);
        url.searchParams.delete("type");
        url.searchParams.delete("index");
        if (push) {
            window.history.pushState(null, "Critterpedia | Nookdata", url.href);
        } else {
            window.history.replaceState(null, "Critterpedia | Nookdata", url.href);
        }
        document.title = "Critterpedia | Nookdata";
    }
}
var critterpedia_data = get_or_insert(nookdata_data, 'critterpedia', {});
function ready() {
    window.setInterval(update, 5000);
    update();
    /** @type {MDCDialog} */
    var dialogue;
    var dialogue_id;
    for ([dialogue_id, dialogue] of Object.entries(window.dialogues)) {
        dialogue.listen("MDCDialog:closing", () => {
            load_or_unload_dialogue(null, true);
        })
    }
    for (let bug_id = 0; bug_id < 80; bug_id++) {
        let index = bug_id.toString().padStart(2, "0");
        let bug_card = document.getElementById(`card_bugs_${index}`);
        let obtained = get_or_insert(critterpedia_data, `bug_${index}_obtained`, false);
        let modelled = get_or_insert(critterpedia_data, `bug_${index}_modelled`, false);
        if (obtained) {
            bug_card.classList.add('obtained');
        }
        if (modelled) {
            bug_card.classList.add('modelled');
        }
    }
    for (let fish_id = 0; fish_id < 80; fish_id++) {
        let index = fish_id.toString().padStart(2, "0");
        let fish_card = document.getElementById(`card_fish_${index}`);
        let obtained = get_or_insert(critterpedia_data, `fish_${index}_obtained`, false);
        let modelled = get_or_insert(critterpedia_data, `fish_${index}_modelled`, false);
        if (obtained) {
            fish_card.classList.add('obtained');
        }
        if (modelled) {
            fish_card.classList.add('modelled');
        }
    }
}
window.begin_scripts = ready;

function load_window_if_required() {
    var url = new URL(window.location.href);
    var type = url.searchParams.get("type");
    var index = url.searchParams.get("index");
    if (type == "bug") {
        try {
            load_or_unload_dialogue("dialogue_bugs_" + index.padStart(2, "0"), false);
        } catch (err) {
            console.error(err.message);
            load_or_unload_dialogue(null, false);
        }
    } else if (type == "fish") {
        try {
            load_or_unload_dialogue("dialogue_fish_" + index.padStart(2, "0"), false);
        } catch (err) {
            console.error(err.message);
            load_or_unload_dialogue(null, false);
        }
    } else {
        load_or_unload_dialogue(null, false);
    }
}
function open(dialogue) {
    load_or_unload_dialogue(dialogue, true);
}
window.open_critter_info = open;
window.load_window_if_required = load_window_if_required;
window.active_critter_info = null;

window.onpopstate = function (event) {
    load_or_unload_dialogue(event.state, false)
};

function switch_critter(dialogue) {
    // onclick=f"switch_critter('dialogue_{type}_{index - 1:0>2}')'",
    load_or_unload_dialogue(null, true);
    load_or_unload_dialogue(dialogue, false);
}

var search_parameters = {
    name: "",
    location: "",
    size: "",
    available_now_only: false,
    unavailable_soon_only: false,
    unobtained_only: false,
    price_comp: ">=",
    price: "",
};
window.search_parameters = search_parameters;

function search_critters() {
    for (let card_id of card_sets) {
        card = document.getElementById("card_" + card_id)
        card.classList.remove("no-match");
        if (search_parameters.name) {
            if (!card.getAttribute("data-name")
                .includes(search_parameters.name.toLowerCase())) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.location) {
            if (!card.getAttribute("data-location")
                .includes(search_parameters.location.toLowerCase())) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.size && card_id.startsWith("fish")) {
            if (card.getAttribute("data-size") != search_parameters.size) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.available_now_only) {
            if (!eval(card.getAttribute("data-times"))[month][hour]) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.unavailable_soon_only) {
            if (eval(card.getAttribute("data-times"))[(month + 1) % 12].some(available => available)) {
                card.classList.add("no-match");
            }
        }
    }
}