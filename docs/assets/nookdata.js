function get_or_insert(data, key, default_val) {
    return JSON.parse(
        data[key] !== undefined
        ? data[key]
        : data[key] = JSON.stringify(
            default_val
        )
    );
}
function get_data() {
    return get_or_insert(window.localStorage, 'nookdata', {});
}