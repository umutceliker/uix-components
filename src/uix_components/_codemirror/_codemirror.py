from uix_components._basic_alert._basic_alert import basic_alert
from uix.elements import textarea
import types
import uix

uix.html.add_script_source("codemirrorjs","_codemirror.js",False,__file__)
uix.html.add_script_source("codemirrorpython","_codemirror_python.js",False,__file__)
uix.html.add_script_source("codemirror-init","_codemirror_init.js",False,__file__)
uix.html.add_css_file("_codemirror.css",__file__)

class codemirror(uix.Element):
    def __init__(self, id=None, cm_parent_id=None, code=None, func_name=None):
        super().__init__(id=id)
        self.cm_parent_id = cm_parent_id
        self.func_name = func_name
        self.code = code

        with self:
            self.alert= basic_alert(id="comp_alert")
            textarea(id="codemirror").cls("wall hall").on("save", self.on_save)

    def on_save(self, ctx, id, value):
        try:
            modified_code = value.replace("\t", "    ")
            dynamic_module = types.ModuleType("dynamic_module")
            globals().update(vars(dynamic_module))
            exec(modified_code, dynamic_module.__dict__)
            file_example_func = getattr(dynamic_module, self.func_name, None)
            
            if file_example_func:
                with ctx.elements[self.cm_parent_id] as parent_container:
                    file_example_func()
                    parent_container.update()        
                self.show_alert("alert-success", "Code executed successfully") 
            else:
                self.show_alert("alert-danger", f"Function {self.func_name} not found in code")

        except SyntaxError as syntax_err:
            self.show_alert("alert-danger", f"Syntax Error: {syntax_err}")

        except NameError as name_err:
            self.show_alert("alert-danger", f"Name Error: {name_err}")
            
        except Exception as e:
            self.show_alert("alert-danger", "Error compiling/executing code: " + str(e))

    def init(self):
        self.session.queue_for_send(self.id, {"string": self.code}, "codemirror-init")
    
    def show_alert(self, alert_type, message):
        self.alert.open(alert_type, message)
