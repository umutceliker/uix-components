from uix.elements import label,input
import uix 

uix.html.add_css_file("_toggle_checkbox.css",__file__)


class toggle_checkbox(label):
    def __init__(self,
            id=None,
            onChange=None,
            input_id=None,
            input_name=None,
            label_usefor=None,
            toggle_on=None,
            toggle_off=None,
            **kwargs):
        super().__init__( id=id, **kwargs)
        self.onChange = onChange
        self.input_id = input_id
        self.input_name = input_name
        self.label_usefor = label_usefor
        self.toggle_on = toggle_on
        self.toggle_off = toggle_off
        self.cls("toggle")

        with self:
            self.toggle = input(
                type="checkbox",
                id=input_id,
                name=input_name,
            ).cls("toggle-check").on("change", onChange)
            
            # to get checked value of checkbox input
            self.toggle.value_name = "checked"
            
            with label(
                usefor=label_usefor
            ).cls("toggle-slider"):
                self.labels = label().cls("labels")
                self.labels.attrs["data-on"] = toggle_on
                self.labels.attrs["data-off"] = toggle_off
        

        
