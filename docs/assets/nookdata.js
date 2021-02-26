function get_or_insert(data, key, default_val) {
    return (
        data[key] !== undefined
            ? data[key]
            : data[key] = default_val
    );
}

if (window.localStorage.nookdata === undefined) {
    window.localStorage.nookdata = "{}";
}

var nookdata_data = JSON.parse(window.localStorage.nookdata);

function save() {
    window.localStorage.nookdata = JSON.stringify(nookdata_data);
}

window.setInterval(save, 30 * 60000);

window.onbeforeunload = function (event) {
    // Save data before page unload
    save();
}
