import uix
import os
from uix.elements import col, button, dialog, image, svg

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

close_btn_svg='<g><path fill="#ffffffff" d="M195.2 195.2a64 64 0 0 1 90.496 0L512 421.504 738.304 195.2a64 64 0 0 1 90.496 90.496L602.496 512 828.8 738.304a64 64 0 0 1-90.496 90.496L512 602.496 285.696 828.8a64 64 0 0 1-90.496-90.496L421.504 512 195.2 285.696a64 64 0 0 1 0-90.496z"/></g>'

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
                    svg(close_btn_svg).size(20,20).viewbox("0,0,1024,1024")
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