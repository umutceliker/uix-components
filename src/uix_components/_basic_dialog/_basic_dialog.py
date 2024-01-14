import uix
import os
from uix.elements import col,button,dialog,image
path = os.path.join(os.path.dirname(__file__))
print(path)
uix.app.add_static_route("close_icon", path)

uix.html.add_css("dialog.css","""
    .dialog-container{
        width: fit-content;
        height: fit-content;
        align-items: flex-end;
        background-color: var(--background);
        gap: 10px;
        justify-content: flex-start;
        padding: 10px;
        border-radius: 6px;
        min-height:50%;
    }
    .dialog-container button{
        background-color: red;
        min-width: 0 !important;
        width: 30px;
        height: 30px;
    }
                  """)

class basic_dialog(dialog):
    def __init__(self,
                id=None,
                elements=None,
                close_on_outside = True, 
                **kwargs
                ):
        super().__init__(id=id, **kwargs)
        self.close_on_outside = close_on_outside
        self.dialog_elements = elements
        self.btnID = id + "-btn"
        with self:
            self.cls("dialog-container")
            with col(id="dialog-column"):
                with button("",id = self.btnID).on("click", lambda ctx, id, value: ctx.elements[self.id].hide()):
                    image("close_icon/close_icon.svg").size(20,20)
                for element in self.dialog_elements:
                    element()


title = "Basic Dialog"

description = """
# basic_dialog(id, elements, close_on_outside = True)
1. Basic Dialog bir dialog komponentidir.
    | attr          | desc                                                |
    | :------------ | :------------------------------------------------   |
    | id            | Komponentin id'si                                   |
    | elements      | Dialog içindeki komponentler                        |
    | close_on_outside | Dışarı tıklandığında kapanma durumu              |

"""
sample="""
from uix.elements import button
from uix_components import basic_dialog
from .basic_checkbox_example import basic_checkbox_example

def basic_dialog_example():
    button("Open Dialog", id = "openDialog").style("width","min-content").on("click", lambda ctx, id, value: ctx.elements["myDialog"].show())
    basic_dialog(id = "myDialog",elements=[basic_checkbox_example], close_on_outside = True)
"""