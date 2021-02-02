var canvases = {};
/** @type {String[]} */
var card_sets = [];
var now = new Date();
var hour = now.getHours();
var minute = now.getMinutes();
var second = now.getSeconds();
var month = (now.getMonth() + 11) % 12;
var month_offset = 0;
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
            let card = document.getElementById(`card_${card_id}`);
            let icon = document.getElementById(`icon_${card_id}`);
            if (card.months[(new_month + month_offset) % 12] && !card.months[(new_month + month_offset + 1) % 12]) {
                icon.innerText = 'warning';
                card.title = card.name.replace(/(?<=^|\s)\w/g, (match) => (match.toUpperCase())); + '\nUnavailable next month';
                card.classList.add('danger');
            } else {
                icon.innerText = 'help';
                card.title = card.name.replace(/(?<=^|\s)\w/g, (match) => (match.toUpperCase()));;
                card.classList.remove('danger');
                card.classList.remove('unavailable');
                if (!card.months[(new_month + month_offset) % 12]) {
                    card.title += '\nUnavailable';
                    card.classList.add('unavailable');
                }
            }
            if (card.modelled) {
                card.title += '\nModel obtained!';
            }
            card.title += '\nClick for more details';
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
var obtained_bugs = 0;
var modelled_bugs = 0;
var obtained_fish = 0;
var modelled_fish = 0;
var critterpedia_data = get_or_insert(nookdata_data, 'critterpedia', {});
function ready() {
    document.body.setAttribute('hemisphere', get_or_insert(nookdata_data, 'hemisphere', 'north'));
    if (nookdata_data.hemisphere == 'south') {
        month_offset = 6;
    }
    for (let bug_id = 0; bug_id < 80; bug_id++) {
        let index = bug_id.toString().padStart(2, "0");
        let bug_card = document.getElementById(`card_bugs_${index}`);
        // data-times
        bug_card.times = JSON.parse(bug_card.getAttribute('data-times'));
        bug_card.months = bug_card.times.map((val) => (val.some((val) => (val))));
        // data-name
        bug_card.name = bug_card.getAttribute('data-name');
        // data-dry
        bug_card.dry = JSON.parse(bug_card.getAttribute('data-dry'));
        // data-rain
        bug_card.rain = JSON.parse(bug_card.getAttribute('data-rain'));
        // data-price
        bug_card.price = JSON.parse(bug_card.getAttribute('data-price'));
        // data-location
        bug_card.location = bug_card.getAttribute('data-location');
        let obtained = get_or_insert(critterpedia_data, `bug_${index}_obtained`, false);
        let modelled = get_or_insert(critterpedia_data, `bug_${index}_modelled`, false);
        bug_card.obtained = obtained;
        bug_card.modelled = modelled;
        let obtain_checkbox = document.getElementById(`checkbox_obtain_bugs_${index}__root`).mdc_checkbox;
        let model_checkbox = document.getElementById(`checkbox_model_bugs_${index}__root`).mdc_checkbox;
        if (obtained) {
            obtain_checkbox.checked = true;
            model_checkbox.disabled = false;
            obtained_bugs++;
            bug_card.classList.add('obtained');
        }
        if (modelled) {
            model_checkbox.checked = true;
            modelled_bugs++;
            bug_card.classList.add('modelled');
        }
        let icon = bug_card.firstChild.firstChild.firstChild.firstChild;
        if (bug_card.months[(month + month_offset) % 12] && !bug_card.months[(month + month_offset + 1) % 12]) {
            icon.innerText = 'warning';
            bug_card.classList.add('danger');
        } else {
            icon.innerText = 'help';
            if (!bug_card.months[(month + month_offset) % 12]) {
                bug_card.classList.add('unavailable');
            }
        }
    }
    document.getElementById('obtained_bugs').innerText = obtained_bugs;
    document.getElementById('modelled_bugs').innerText = modelled_bugs;
    for (let fish_id = 0; fish_id < 80; fish_id++) {
        let index = fish_id.toString().padStart(2, "0");
        let fish_card = document.getElementById(`card_fish_${index}`);
        // data-times
        fish_card.times = JSON.parse(fish_card.getAttribute('data-times'));
        fish_card.months = fish_card.times.map((val) => (val.some((val) => (val))));
        // data-name
        fish_card.name = fish_card.getAttribute('data-name');
        // data-dry
        fish_card.dry = JSON.parse(fish_card.getAttribute('data-dry'));
        // data-rain
        fish_card.rain = JSON.parse(fish_card.getAttribute('data-rain'));
        // data-price
        fish_card.price = JSON.parse(fish_card.getAttribute('data-price'));
        // data-size
        fish_card.size = JSON.parse(fish_card.getAttribute('data-size'));
        // data-location
        fish_card.location = fish_card.getAttribute('data-location');
        let obtained = get_or_insert(critterpedia_data, `fish_${index}_obtained`, false);
        let modelled = get_or_insert(critterpedia_data, `fish_${index}_modelled`, false);
        fish_card.obtained = obtained;
        fish_card.modelled = modelled;
        let obtain_checkbox = document.getElementById(`checkbox_obtain_fish_${index}__root`).mdc_checkbox;
        let model_checkbox = document.getElementById(`checkbox_model_fish_${index}__root`).mdc_checkbox;
        if (obtained) {
            obtain_checkbox.checked = true;
            model_checkbox.disabled = false;
            obtained_fish++;
            fish_card.classList.add('obtained');
        }
        if (modelled) {
            model_checkbox.checked = true;
            modelled_fish++;
            fish_card.classList.add('modelled');
        }
        let icon = fish_card.firstChild.firstChild.firstChild.firstChild;
        if (fish_card.months[(month + month_offset) % 12] && !fish_card.months[(month + month_offset + 1) % 12]) {
            icon.innerText = 'warning';
            fish_card.classList.add('danger');
        } else {
            icon.innerText = 'help';
            if (!fish_card.months[(month + month_offset) % 12]) {
                fish_card.classList.add('unavailable');
            }
        }
    }
    document.getElementById('obtained_fish').innerText = obtained_fish;
    document.getElementById('modelled_fish').innerText = modelled_fish;
    for (let card_id of card_sets) {
        for (let month = 0; month < 12; month++) {
            let month_card = document.getElementById(`card_${month}_${card_id}`);
            let card = document.getElementById(`card_${card_id}`);
            if (card.months[(month + month_offset) % 12]) {
                month_card.classList.remove('card-inactive');
            } else {
                month_card.classList.add('card-inactive');
            }
        }
    }
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
}
window.begin_scripts = ready;

function mark_obtained(set_id, obtained) {
    let card = document.getElementById('card_' + set_id);
    let model_checkbox = document.getElementById('checkbox_model_' + set_id + '__root').mdc_checkbox;
    card.obtained = obtained;
    if (obtained) {
        model_checkbox.disabled = false;
        card.classList.add('obtained');
        if (set_id.startsWith('bug')) {
            obtained_bugs++;
        } else { obtained_fish++; }
        document.getElementById('obtained_bugs').innerText = obtained_bugs;
        document.getElementById('obtained_fish').innerText = obtained_fish;
    } else {
        if (model_checkbox.checked) {
            model_checkbox.checked = false;
            mark_modelled(set_id, false);
        }
        model_checkbox.disabled = true;
        card.classList.remove('obtained');
        if (set_id.startsWith('bug')) {
            obtained_bugs--;
        } else { obtained_fish--; }
        document.getElementById('obtained_bugs').innerText = obtained_bugs;
        document.getElementById('obtained_fish').innerText = obtained_fish;
    }
    critterpedia_data[set_id.replace('bugs', 'bug') + '_obtained'] = obtained;
}
function mark_modelled(set_id, modelled) {
    let card = document.getElementById('card_' + set_id);
    card.modelled = modelled;
    if (modelled) {
        card.classList.add('modelled');
        if (set_id.startsWith('bug')) {
            modelled_bugs++;
        } else { modelled_fish++; }
        document.getElementById('modelled_bugs').innerText = modelled_bugs;
        document.getElementById('modelled_fish').innerText = modelled_fish;
    } else {
        card.classList.remove('modelled');
        if (set_id.startsWith('bug')) {
            modelled_bugs--;
        } else { modelled_fish--; }
        document.getElementById('modelled_bugs').innerText = modelled_bugs;
        document.getElementById('modelled_fish').innerText = modelled_fish;
    }
    critterpedia_data[set_id.replace('bugs', 'bug') + '_modelled'] = modelled;
    if (card.months[(month + month_offset) % 12] && !card.months[(month + month_offset + 1) % 12]) {
        card.title = card.name.replace(/(?<=^|\s)\w/g, (match) => (match.toUpperCase())); + '\nUnavailable next month';
    } else {
        card.title = card.name.replace(/(?<=^|\s)\w/g, (match) => (match.toUpperCase()));;
        if (!card.months[(month + month_offset) % 12]) {
            card.title += '\nUnavailable';
        }
    }
    if (card.modelled) {
        card.title += '\nModel obtained!';
    }
    card.title += '\nClick for more details';
}

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
        card = document.getElementById("card_" + card_id);
        card.classList.remove("no-match");
        if (search_parameters.name) {
            if (!card.name
                .includes(search_parameters.name.toLowerCase())) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.location) {
            if (!card.location
                .includes(search_parameters.location.toLowerCase())) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.size && card_id.startsWith("fish")) {
            if (card.size != search_parameters.size) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.available_now_only) {
            if (!card.times[month][hour]) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.unavailable_soon_only) {
            if (card.months[(month + 1) % 12] || !card.months[month]) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.unobtained_only) {
            if (card.obtained) {
                card.classList.add("no-match");
            }
        }
        if (search_parameters.price) {
            if (search_parameters.price_comp == '>=') {
                if (card.price < search_parameters.price) {
                    card.classList.add("no-match");
                }
            } else if (search_parameters.price_comp == '<=') {
                if (card.price > search_parameters.price) {
                    card.classList.add("no-match");
                }
            } else if (search_parameters.price_comp == '=') {
                if (card.price != search_parameters.price) {
                    card.classList.add("no-match");
                }
            }
        }
    }
}
const price_dropdown = document.getElementById('critter-price-comp').mdc_dropdown;
price_dropdown.listen('MDCSelect:change', () => {
    search_parameters.price_comp = price_dropdown.value;
    search_critters();
});