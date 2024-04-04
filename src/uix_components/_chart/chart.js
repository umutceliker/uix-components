event_handlers["init-chart"] = function (id, value, event_name) {
    
    let chart = new Chart(id, value);
    elm = document.getElementById(id);
    elm.chart = chart;
}
