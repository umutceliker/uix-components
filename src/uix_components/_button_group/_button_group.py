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
                        self.link.cls(value.get("btn_classes"))
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
        
    def show(self):
        self.set_style("display","flex")