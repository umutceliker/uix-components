from uix.elements import unorderedlist, listitem, label, summary, details
import uix

uix.html.add_css_file("_tree_view.css",__file__)

class tree_view(uix.Element):
    def __init__(self, id=None, data=None, callback=None, selected_label=None):
        super().__init__(id=id)
        self.data = data or {}
        self.callback = callback
        self.selected_label = selected_label

        with self:
            with unorderedlist().cls("tree"):
                for main_title, items in self.data.items():
                    self.create_tree(main_title, items, main_title == list(self.data.keys())[0])  

    def create_tree(self, key, data, isOpen=False):
        with listitem(id=f"li-{key.lower()}"):
            with details(id=f"details-{key}").cls("details") as detail:
                if isOpen:
                    detail.attrs["open"] = "True"
                summary(value=key.title())

                if isinstance(data, list):
                    with unorderedlist():
                        for item in data:
                            self._create_list_item(item)
                else:
                    with unorderedlist():
                        for sub_key, sub_data in data.items():
                            self.create_tree(sub_key, sub_data)

    def _create_list_item(self, item):
        with listitem().cls("last-child"):
            if isinstance(item, dict):
                name, id_value = next(iter(item.items()))  
            else:
                name, id_value = item, item  
            
            label_class = "selected-label" if self.selected_label == id_value else ""
            label_ = label(id=id_value, value=name).cls(label_class).style("font-size: medium;")
            
            if self.callback:
                label_.on("click", self.click_label) 

    def click_label(self, ctx, id_value, name):  
        self.callback(ctx, id_value, name) 



title="Tree View"
description="""
## tree_view(id, data, callback, selected_label)
1. Verilen veri yapısına göre ağaç yapısı oluşturur.
2. Veri yapısı içindeki her bir anahtar bir başlık olarak kullanılır.
3. Anahtarın değeri bir liste ise, liste elemanları alt başlık olarak kullanılır.
4. Anahtarın değeri bir sözlük ise, id ve label değerlerini kullanarak alt ağaç oluşturulur.
5. Label'a tıklandığında callback fonksiyonu çalışır.


| attr                  | desc                                                 |
| :-------------------- | :------------------------------------------------    |
| id                    | tree_view elementinin id'si                          |
| data                  | ağaç yapısının oluşturulması için gerekli veri yapısı|
| callback              | Label'a tıklandığında çalışacak fonksiyon            |
| selected_label        | Önceden seçili olmasını istediğiniz elemanın değeri  |
"""
sample="""
from uix_components import tree_view
from uix.core.session import context
from uix.elements import text, div, row

data = {
    "Examples": {
        "Styles": {
            "Colors": ["Red", "Green"],
            "Shapes": ["Circle", "Square"]
        },
        "Components": ["Select", "Tree View"]
    }
 }
# label id'si ve label değeri olan bir veri yapısı
data2 = {
    "Examples": {
        "Colors": [{
            "Red": "red-id",
            "Blue": "blue-id"
        }],
        "Shapes": [{
            "Circle": "circle-id",
            "Square": "square-id"
        }]
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
    with div():
        with row().style("gap","20px"):
            tree_view(id="tree_1",data=data, callback= select_label)
            tree_view(id="tree_2",data=data2, callback= select_label)
        text("Selected Value:", id="output")
        open_components()
"""