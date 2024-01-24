import uix
from uix.elements import check, label

uix.html.add_css("checkbox.css","""
    .checkbox-container{
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 5px;
    }""")

class basic_checkbox(uix.Element):
    def __init__(
            self,
            id=None,
            label_text=None,
            value=None,
            callback=None,
            **kwargs
        ):
        super().__init__(id=id, **kwargs) # value won't be sent to super class, only used to set checkbox value
        self.label = label_text
        self.callback = callback
        self.checkboxID = id + "-checkbox"
        self.labelID = id + "-label"
        self.cls("checkbox-container")

        with self:
            self.checkbox = check(id=self.checkboxID, value=value).on("click", self.set_value)
            label(usefor=self.checkbox.id, value=self.label)

    def set_value(self, ctx, id, value):
        self.checkbox.value = value
        if self.callback:
            self.callback(ctx,id, value)

title = "Basic Checkbox"

description = """
# basic_checkbox(id, label_text, value, callback)
1. Basic Checkbox bir checkbox komponentidir.
    | attr          | desc                                                |
    | :------------ | :------------------------------------------------   |
    | id            | Komponentin id'si                                   |
    | label_text    | Komponentin yanındaki yazı                          |
    | value         | Komponentin değeri                                  |
    | callback      | Komponentin değeri değiştiğinde çalışacak fonksiyon |
"""

sample="""
from uix.elements import text
from uix_components import basic_checkbox

def on_change(ctx,id,value):
    ctx.elements["test"].value = value
    ctx.elements["test"].update()

def basic_checkbox_example():
    basic_checkbox(id = "myCheckbox",label_text="Label Text",callback=on_change)
    text(id="test", value="Checkbox Value")

"""
