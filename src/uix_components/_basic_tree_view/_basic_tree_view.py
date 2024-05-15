from uix.elements import unorderedlist, listitem, label, div, check
import uix
uix.html.add_css_file("_basic_tree_view.css",__file__)

class basic_tree_view(uix.Element):
    def __init__(self, id, data):
        super().__init__(id=id)
        if data is None:
            data = {}
        
        def create_tree(key, data, component):
            with listitem(id="li-"+key.lower()).style("list-style","none"):
                label_attributes = {"usefor": "trigger-" + key.lower()}
                check(id="trigger-" + key.lower()).cls("comp_type") 
                self.label = label(value=key, **label_attributes)
                if isinstance(data, dict) and data:
                    self.label.cls("super-class")
                    with self.label:
                        div("").cls("plus").tag = "span"
                    with unorderedlist("").cls("pure-tree"):
                        for sub_key in data:
                            create_tree(sub_key, data[sub_key], component)
        
        with self:
            with unorderedlist("").cls("pure-tree main-tree"):
                for main_title in data:
                    create_tree(main_title, data[main_title], check)