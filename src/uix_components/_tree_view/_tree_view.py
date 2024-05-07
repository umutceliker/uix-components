from uix.elements import unorderedlist, listitem, label, summary, details
import uix

uix.html.add_css_file("_tree_view.css",__file__)

class tree_view(uix.Element):
    def __init__(self, id, data, callback=None):
        super().__init__(id=id)
        if data is None:
            data = {}
        self.titles = list(data.keys()) 
        self.callbak = callback
        with self:
            with unorderedlist().cls("tree"):
                for main_title, items in data.items():
                    
                    self.create_tree(main_title, items)
        
    def create_tree(self, key, data):
        with listitem(id="li-" + key.lower()):

            with details().cls("details") as detail:
                if self.titles[0] == key:
                    detail.attrs["open"] = "True"
                summary(value=key.title()) 

                if isinstance(data, list):
                    with unorderedlist():
                        for item in data:
                            with listitem().cls("last-child"):
                                label(value=item).on("click", self.click_label).style("font-size","medium")
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
"""
sample="""
from uix_components._tree_view._tree_view import title, description, sample as code 
from uix_components import tree_view
from uix.elements import text, div

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

def tree_view_example():
    with div().cls("gap"):
        tree_view(id="tree_view_example",data=data, callback= select_label)
        text("Selected Value:", id="output")
"""