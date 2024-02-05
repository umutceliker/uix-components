from uix.elements import row, button, icon, text,link
import uix

uix.html.add_css_file("_button_group.css",__file__)

class button_group(row):
    def __init__(self,
            id=None,
            items:dict=None,
            **kwargs):
        super().__init__( id=id  ,**kwargs)

        self.cls("row-group")
        self.style("width","fit-content !important").style("display","flex")
        with self:
            for key, value in items.items():
                row_styles = value.get("row_styles", {})
                for row_style_key, row_style_value in row_styles.items():
                    self.style(row_style_key, row_style_value)
                row_classes = value.get("row_classes")
                self.cls(row_classes)

                self.btn_id = value.get("btn_id")
                if value.get("link") is not None:
                    with link("",id=self.btn_id,href=value.get("link")) as _link:
                        self.link=_link
                        if value.get("download") is True:
                            name=value.get("link").split("/")[-1]
                            self.link.attrs["download"]=name
                        self.get_buttonGroup(value)
                else:
                        self.get_buttonGroup(value)
    def get_buttonGroup(self, value):
        with button("",id=self.btn_id).cls("btn-group") as btn:
            if value.get("onClick") is not None:
                btn.on("click", value.get("onClick"))
            btn_styles = value.get("btn_styles", {})
            for style_key, style_value in btn_styles.items():
                btn.style(style_key, style_value)
            btn_classes = value.get("btn_classes")
            btn.cls(btn_classes)

            if value.get("icon") is not None:
                with icon(value=value.get("icon")).cls("fa-icon") as icons:
                    icon_styles = value.get("icon_styles", {})
                    for icon_style_key, icon_style_value in icon_styles.items():
                        icons.style(icon_style_key, icon_style_value)

            if value.get("text") is not None:
                with text(value=value.get("text")) as texts:
                    text_styles = value.get("text_styles", {})
                    for text_style_key, text_style_value in text_styles.items():
                        texts.style(text_style_key, text_style_value)
                    text_classes = value.get("text_classes")
                    texts.cls(text_classes)

    def hide(self):
        self.set_style("display","none")
        print("hide")
        
    def show(self):
        self.set_style("display","flex")
        print("show")
        

title = "Button Group"
description = """
 # button_section(id, items)
 1. Button Section bir button komponentidir. Style'lar dict, class'lar string olarak verilir.
    | attr          | desc                                                            |
    | :------------ | :-----------------------------------------------------          |
    | id            | Komponentin id'si                                               |
    | items         | Komponentin içindeki iconların dict olarak verilmesi gerekiyor. |
    | onClick       | Komponentin değeri değiştiğinde çalışacak fonksiyon             |
    | row_classes   | Komponentin içine row class tanımlamak için kullanılır.         |
    | row_styles    | Komponentin içine row style tanımlamak için kullanılır.         |
    | icon_styles   | Komponentin içine icon style tanımlamak için kullanılır.        |
    | btn_classes   | Komponentin içine button class tanımlamak için kullanılır.      |
    | btn_styles    | Komponentin içine button style tanımlamak için kullanılır.      |
    | btn_id        | Komponentin içine button id tanımlamak için kullanılır.         |
    | text_styles   | Komponentin içine text style tanımlamak için kullanılır.        |
    | text_classes  | Komponentin içine text class tanımlamak için kullanılır.        |
"""
sample="""
from uix_components import button_section

def icon_func1(ctx, id, value):
    ctx.elements["text1"].value = "icon_func1"

def icon_func2(ctx, id, value):
    ctx.elements["text1"].value = "icon_func2"

icon_btn_group = {
    "icon-btn-1": {
        "icon": "fa-solid fa-trash",
        "onClick": icon_func1,
        "row_styles": {"width": "min-content"},
        "icon_styles": {"font-size": "20px", "color": "red"},
        "btn_styles": {},
    },
    "icon-btn-2": {
        "icon": "fa-sharp fa-solid fa-circle-info",
        "onClick": icon_func2,
    },
    "icon-btn-3": {
        "icon": "fa-solid fa-download",
        "onClick": icon_func2,
    }
}

text_btn_group = {
    "text-btn-1": {
        "text": "Download",
        "onClick": icon_func1,
        "row_styles": {"background-color": "white"},
        "btn_styles": {"background-color": "black"},
        "icon": "fa-solid fa-download",
    },
    "text-btn-2": {
        "text": "Button 2",
        "onClick": icon_func2,
        "btn_styles": {"background-color": "black"},
    },
    "text-btn-3": {
        "text": "Button 3",
        "onClick": icon_func2,
        "btn_styles": {"background-color": "black"},
        "text_styles": {"color": "red"},
    }
}

def button_group_example():
        with col().style("gap","5px"): 
            button_group(items=icon_btn_group,id="custom-button-section-1")
            button_group(items=text_btn_group,id="custom-button-section-2")
            text("",id="text1")
"""