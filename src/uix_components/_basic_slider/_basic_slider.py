import uix
from uix.elements import slider, input, row, text

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
uix.html.add_css("basic_slider_css","""
.basic-slider {
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
    flex-direction: column;
    gap: 5px;
}
.basic-slider-input {
    width: 30px;
    text-align: center;
}
""")
class basic_slider(uix.Element):
    def __init__(self,name, id = None, min = 0, max = 100, value = 50, step = 1,callback = None):
        super().__init__("",id = id)
        self.sliderID = id + "-slider"
        self.inputID = id + "-input"
        self.max=max
        self.min=min
        self.callback = callback
        self.cls("basic-slider")
        with self:
            with row().cls("wall hall").style("justify-content","space-between"):
                text(name)
                self.input=input(type="number", id = self.inputID, value = value).cls("basic-slider-input").on("input", self.on_slider_change)
                self.input.attr("min",min)
                self.input.attr("max",max)
                self.input.attr("step",step)
            with row():
                self.slider=slider(id = self.sliderID, min=min, max=max, value=value, step=step).on("input", self.on_slider_change).style("width","100%")

    def on_slider_change(self,ctx, id, value):
        if self.callback:
            self.callback(ctx, id, value)
       
    def init(self):
        print("basic_slider init")
        self.session.queue_for_send("init-slider", {"sliderID": self.sliderID, "inputID": self.inputID},"init-slider")