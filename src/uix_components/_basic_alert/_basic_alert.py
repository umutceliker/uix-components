import uix
from uix.elements import text, div

uix.html.add_css_file("_basic_alert.css",__file__)

uix.html.add_script("_basic_alert.js","""
event_handlers["alert-open"] = function(id, value, event_name){
    var alertContainer = document.getElementById("comp_alert");

    var alertDiv = document.createElement("div");
    alertDiv.className = value.type + " alert-child alert-close";
    alertDiv.textContent = value.message;
                    
    const progressBar = document.createElement("div");
                    
    progressBar.className = "alert-progress";
    alertDiv.appendChild(progressBar);
                    
    if(value.icon != null){
        const icon = document.createElement("i");
        icon.className = value.icon;
        alertDiv.appendChild(icon);
    }

    alertContainer.appendChild(alertDiv);

    alertDiv.addEventListener("animationend", function(){
        alertContainer.removeChild(alertDiv);
    });             
}
                    
    """, beforeMain=False)

class basic_alert(uix.Element):
    def __init__(self, value=None, id=None, type="normal"):
        super().__init__(value, id=id)

        self.cls("alert")

    def open(self, type, value, icon=None):
        opt = {
            "type": type,
            "message": value,
            "icon": icon
        }
        self.session.send(self.id, opt, "alert-open")



title = "Basic Alert"

description = """
# basic_alert(id, value, type = ["alert-normal", "alert-success", "alert-info", "alert-warning", "alert-danger"])
1. Basic Alert bir alert komponentidir.
    | attr          | desc                                                |
    | :------------ | :------------------------------------------------   |
    | id            | Komponentin id'si                                   |
    | value         | Komponentin değeri                                  |
    | type          | Komponentin tipi                                    |
"""

sample = """
import uix
import uix_components
from uix.elements import div, button, grid, col
from uix_components import basic_alert
from uix_components._basic_alert._basic_alert import title, description, sample as code 

def alert_example():
    with col() as content:
        alert = basic_alert("", id = "myAlert", type="success", duration=5000)
        button("Show Alert", id = "show_alert").on("click", lambda ctx, id, value: alert.open("alert-success", "selam"))
    return content
"""

