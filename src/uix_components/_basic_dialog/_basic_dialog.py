import uix
from uix.elements import col, button, dialog, icon, row, text

uix.html.add_css("dialog.css","""

    .dialog-container{
        width: 60vw;
        height: 80vh;
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
                 justify-content: space-between;
                    align-items: center;}
                 
""")

class basic_dialog(dialog):
    def __init__(self,
                id=None,
                elements=None,
                close_on_outside = True, 
                close_icon = None,
                close_callback = None,
                title = None,
                **kwargs
                ):
        super().__init__(id=id, **kwargs)
        
        self.close_on_outside = close_on_outside
        self.dialog_elements = elements
        self.btnID = id + "-btn"
        self.close_icon = close_icon
        self.close_callback = close_callback
        self.title = title

        with self:
            self.cls("dialog-container")
            with col(id="dialog-column").style("gap","20px"):
                with row("").cls("dialog-header"):
                    if self.title:
                        text(value=self.title).style("font-size","1.5rem").style("font-weight","bold")
                    else:
                        text(value="")
                    with button("",id = self.btnID).cls("dialog-container-button").on("click", self.close) as self.close_btn:
                        if close_icon:
                            icon(self.close_icon, id=self.btnID + "-icon")
                        else:
                            icon("fa-solid fa-xmark", id=self.btnID + "-icon" ).style("font-size","20px")
                for element in self.dialog_elements:
                    element()

    def close(self, ctx, id, value):
        ctx.elements[self.id].hide()
        if self.close_callback:
            self.close_callback(ctx, id, value)