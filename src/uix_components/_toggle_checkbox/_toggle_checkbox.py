from uix.elements import label,input
from uix import T
import uix 
uix.html.add_css_file("_toggle_checkbox.css",__file__)

class toggle_checkbox(label):
    def __init__(self,
                 id=None,
                 onChange=None,
                 input_id=None,
                 input_name=None,
                 label_usefor=None,
                 toggle_on="",
                 toggle_off="", **kwargs):
        super().__init__(id=id, **kwargs)
        self.cls("toggle")
       
        with self:
            self.toggle = input(
                type="checkbox",
                id=input_id,
                name=input_name,
            ).cls("toggle-check").on("change", onChange)
            
            # Set the value name for the checkbox input
            self.toggle.value_name = "checked"
            
            with label(usefor=label_usefor).cls("toggle-slider"):
                self.labels = label().cls("labels")
                self.labels.attrs["data-on"] = T(toggle_on)
                self.labels.attrs["data-off"] = T(toggle_off)
