from uix.elements import unorderedlist, listitem, label, summary, details
import uix

uix.html.add_css_file("_tree_view.css",__file__)

class tree_view(uix.Element):
    def __init__(self, id=None, data=None, callback=None, selected = None):
        super().__init__(id=id)
        if data is None:
            data = {}
        self.titles = list(data.keys()) 
        self.callbak = callback
        self.selected = selected
        with self:
            with unorderedlist().cls("tree"):
                for main_title, items in data.items():
                    
                    self.create_tree(main_title, items)
        
    def create_tree(self, key, data):
        with listitem(id="li-" + key.lower()):

            with details(id="details-" + key).cls("details") as detail:
                if self.titles[0] == key:
                    detail.attrs["open"] = "True"
                summary(value=key.title()) 

                if isinstance(data, list):
                    with unorderedlist():
                        for item in data:
                            if isinstance(item, dict):
                                for name, id in item.items():
                                    with listitem().cls("last-child"):
                                        if self.selected and id == self.selected:
                                            label_ = label(id = id,value = name).cls("selected-label")
                                        else:
                                            label_ = label(id = id,value = name)
                            else:
                                with listitem().cls("last-child"):
                                    if self.selected and item == self.selected:
                                        label_ = label(id=item,value=item).cls("selected-label")
                                    else:
                                        label_ = label(id=item,value=item)
                            label_.style("font-size","medium")
                            if self.callbak:    
                                label_.on("click", self.click_label)
                else: 
                    with unorderedlist():
                        for sub_key, sub_data in data.items():
                            self.create_tree(sub_key, sub_data) 

    def click_label(self, ctx, id, value):
        self.callbak(ctx, id, value)



title="Tree View"
description="""
## tree_view(id, data)
1. Verilen veri yapısına göre ağaç yapısı oluşturur.
2. Veri yapısı içindeki her bir anahtar bir başlık olarak kullanılır.

| attr                  | desc                                                 |
| :-------------------- | :------------------------------------------------    |
| id                    | tree_view elementinin id'si                          |
| data                  | ağaç yapısının oluşturulması için gerekli veri yapısı|
| callback              | Label'a tıklandığında çalışacak fonksiyon            |
| selected              | Önceden seçili olmasını istediğiniz elemanın değeri  |
"""
sample="""
data = {
    "Examples": {
        "Styles": {
            "Colors": ["Red", "Green"],
            "Shapes": ["Circle", "Square"]
        },
        "Components": ["Select", "Tree View"]
    }
 }

def select_label(ctx, id, value):
    ctx.elements["output"].value = f'Selected Value: {value}'

def open_components():
    ctx = context.session.context
    # Açık olmasını istediğiniz details elementinin id'si
    # Default olarak "details-" ile başlar
    ctx.elements["details-Components"].attrs["open"] = "True"

def tree_view_example():
    with div().cls("gap"):
        tree_view(id="tree_view_example",data=data, callback= select_label)
        text("Selected Value:", id="output")
        open_components()
"""