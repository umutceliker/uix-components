import uix
from uix.elements import text

uix.html.add_css_file("_basic_alert.css",__file__)

class basic_alert(uix.Element):
    def __init__(self, value=None, id=None, type="normal"):
        super().__init__(value, id=id)

        self.type = type
        self.current_type = "alert-normal"

        with self.cls("alert container" + self.current_type).on("click", self.close):
            self.text = text(value=self.value, id=self.id + "_text")
        
    def setBaseStyle(self):
        self.classes = ["alert" , "container"]

    def close(self, ctx, id, value):
        self.setBaseStyle()
        self.cls("alert-end")
        self.current_type = self.type
        self.update()

    def open(self, type, message):
        self.setBaseStyle()
        self.current_type = type
        self.cls(self.current_type)
        self.text.value = message
        self.cls("alert-start")
        self.update()

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

