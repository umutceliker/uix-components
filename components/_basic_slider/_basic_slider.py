import uix
from uix.elements import slider, border, input, canvas

uix.html.add_script("slider","""
    event_handlers["init-slider"] = function(id, value, event_name) {
        document.getElementById(value.sliderID).addEventListener("input", function(e) {
            document.getElementById(value.inputID).value = e.target.value;
        });
        document.getElementById(value.inputID).addEventListener("change", function(e) {
            document.getElementById(value.sliderID).value = e.target.value;
        });
    };
""",False)

class basic_slider(uix.Element):
    def __init__(self,name, id = None, min = 0, max = 100, value = 50, step = 1,callback = None):
        super().__init__(name,id = id)
        self.sliderID = id + "-slider"
        self.inputID = id + "-input"
        self.callback = callback
        self.cls("border")
        with self:
            slider(id = self.sliderID, min=min, max=max, value=value, step=step).on("change", self.on_slider_change)
            input(type="number", id = self.inputID, value = value).style("width","30px;").on("change", self.on_slider_change)

    def on_slider_change(self,ctx, id, value):
        if self.callback:
            self.callback(ctx, id, value)
       
    def init(self):
        print("basic_slider init")
        self.session.queue_for_send("init-slider", {"sliderID": self.sliderID, "inputID": self.inputID},"init-slider")
 