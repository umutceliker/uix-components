from uix.elements import row, button, icon
import uix

uix.html.add_css_file("_custom_button_section.css",__file__)

class custom_button_section(row):
    def __init__(self,
            id=None,
            items:dict=None,
            **kwargs):
        super().__init__( id=id  ,**kwargs)

        self.cls("row-section")
        with self:
            for key, value in items.items():
                row_styles = value.get("styles", {})
                for row_style_key, row_style_value in row_styles.items():
                    self.style(row_style_key, row_style_value)

                with button("").cls("btn-section").on("click", value.get("onClick")) as btn:
                    btn_styles = value.get("btn_styles", {})
                    for style_key, style_value in btn_styles.items():
                        btn.style(style_key, style_value)
                        
                    with icon(value=value.get("icon")).cls("fa-icon") as icons:
                        icon_styles = value.get("icon_styles", {})
                        for icon_style_key, icon_style_value in icon_styles.items():
                            icons.style(icon_style_key, icon_style_value)


title = "Button Section"
description = """
 # button_section(id, items)
 1. Button Section bir button komponentidir.
    | attr          | desc                                                            |
    | :------------ | :-----------------------------------------------------          |
    | id            | Komponentin id'si                                               |
    | items         | Komponentin içindeki iconların dict olarak verilmesi gerekiyor. |
    | onClick       | Komponentin değeri değiştiğinde çalışacak fonksiyon             |
    | row_styles    | Komponentin içindeki row style tanımlamak için kullanılır.      |
    | icon_styles   | Komponentin içindeki icon style tanımlamak için kullanılır.     |
    | btn_styles    | Komponentin içindeki button style tanımlamak için kullanılır.   |
"""
sample="""
from uix_components import button_section

def icon_func1(ctx, id, value):
    ctx.elements["text1"].value = "icon_func1"

def icon_func2(ctx, id, value):
    ctx.elements["text1"].value = "icon_func2"

items = {
    "icon1": {
        "icon": "fa-solid fa-trash",
        "onClick": icon_func1,
        "row_styles": {"width": "min-content"},
        "icon_styles": {"font-size": "30px", "color": "red"},
        "btn_styles": {},
    },
    "icon2": {
        "icon": "fa-sharp fa-solid fa-circle-info",
        "onClick": icon_func2,
    },
    "icon3": {
        "icon": "fa-solid fa-download",
        "onClick": icon_func2,
    }
    
}
def custom_button_section_example():
    custom_button_section(items=items,  id="custom-button-section-1")
    text("",id="text1",)
"""