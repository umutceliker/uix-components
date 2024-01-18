import uix
from uix.elements import unorderedlist, listitem,label, div,check,row


uix.html.add_css_file("_basic_tree_view.css",__file__)

class basic_tree_view(uix.Element):
    def __init__(self,id, data, main_title):
        super().__init__(id=id)
        if data == None:
            data = {}
        self.main_title = main_title

        def create_tree(key, data, component):
            with listitem(id="li-"+key.lower()).style("list-style","none"):
                label_attributes = {"usefor": "trigger-" + key.lower()}
                check(id="trigger-" + key.lower()).cls("comp_type") 
                self.label=label(value=key,**label_attributes)
                if isinstance(data, dict) and data:
                    self.label.cls("super-class")
                    with self.label:
                        div("").cls("plus").tag="span"
                    with unorderedlist("").cls("pure-tree"):
                        for sub_key in data:
                            create_tree(sub_key, data[sub_key],component)
        with self:
            with unorderedlist("").cls("pure-tree main-tree"):
                create_tree(main_title, data, check)

title="Basic Tree View"
description="""
## basic_tree_view(id, data)

1- Verilen veri yapısına göre checkbox elementi içeren bir ağaç yapısı oluşturur.

| attr                  | desc                                              |
| :-------------------- | :------------------------------------------------ |
| id                    | basic_tree_view elementinin id'si                         |
| main_title                 | ağaç yapısının başlığı. Örnek: "views" |
| data                  | ağaç yapısının oluşturulması için gerekli veri yapısı. Örnek: {"views":{"view1":{},"view2":{}}} |
"""

sample="""
data = {
    "key1": "value1",
    "key2": "value2",
    "key3": {
        "key4": "value4",
        "key5": "value5",
        "key6": {
            "key7": "value7",
            "key8": "value8",
            "key9": "value9",
        }
    }
}

def basic_tree_example():
    with div() as basic_tree_view_example:
        basic_tree_view(id="basic_tree_view_example",data=data, title="views")
    return basic_tree_view_example"""

        

