import uix
from uix.elements import div, textarea, label, text, embed, col, row
from uix_components._basic_alert._basic_alert import basic_alert
import types

import inspect

uix.html.add_script_source("codemirrorjs","codemirror.js",True,__file__)
uix.html.add_script_source("codemirrorpython","codemirrorpython.js",True,__file__)
uix.html.add_css_file("codemirror.css",__file__)
uix.html.add_script_source("codemirrorinit","codemirrorinit.js",False,__file__)

class codemirror(uix.Element):
    def __init__(self, id=None, value=None, element_to_change = None, item_data=None,item_name=None, **kwargs):
        super().__init__(id=id, **kwargs)
        self.id = "codemirrordeneme"
        self.item_data = item_data
        self.element_to_change = element_to_change
        self.item_name = item_name

        with self.cls("wall hall"):
            self.alert = basic_alert()
            textarea(id="codemirror").cls("wall hall").on("save", self.on_save)
            with div(id="exceptions"): 
                text("").style("color","red")

    def on_save(self, ctx, id, value):
        try:
            value = value.strip()

            dynamic_module = types.ModuleType("dynamic_module")
            globals().update(vars(dynamic_module))

            exec(value, dynamic_module.__dict__)

            file_example_func = getattr(dynamic_module, self.item_name+"_example", None)
            if file_example_func:
                with row(id=self.element_to_change).style("align-items:flex-start; justify-content:center;") as update_container:
                    file_example_func()
            else:
                print("_example function not found in the provided code")

            update_container.update()
        except Exception as e:
            self.alert.open("danger", "Error compiling/executing code: " + str(e))
            print("Error compiling/executing code:", e)

    def init(self):
        self.session.queue_for_send(self.id, {"string":"Selam"}, "codemirrorinit")
