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

window.onbeforeunload = function (event) {
    // Save data before page unload
    window.localStorage.nookdata = JSON.stringify(nookdata_data);
}
