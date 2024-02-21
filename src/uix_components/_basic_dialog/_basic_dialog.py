import uix
from uix.elements import col, button, dialog, icon

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

    }
    .dialog-container-button{
        background-color: red;
        min-width: 0 !important;
        width: 30px;
        height: 30px;
        padding: 0;
    }
    .dialog-header{
                 height: 5%;
                 justify-content: center;
                    align-items: flex-end;}
                 
""")

class basic_dialog(dialog):
    def __init__(self,
                id=None,
                elements=None,
                close_on_outside = True, 
                close_icon = None,
                **kwargs
                ):
        super().__init__(id=id, **kwargs)
        
        self.close_on_outside = close_on_outside
        self.dialog_elements = elements
        self.btnID = id + "-btn"
        self.close_icon = close_icon

        with self:
            self.cls("dialog-container")
            with col(id="dialog-column").style("gap","10px"):
                with col("").cls("dialog-header"):
                    with button("",id = self.btnID).cls("dialog-container-button").on("click", lambda ctx, id, value: ctx.elements[self.id].hide()) as self.close_btn:
                        if close_icon:
                            icon(self.close_icon, id=self.btnID + "-icon")
                        else:
                            icon("fa-solid fa-xmark", id=self.btnID + "-icon" ).style("font-size","20px")
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