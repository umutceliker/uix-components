from uix.elements import unorderedlist, listitem, label, summary, details
import uix

uix.html.add_css_file("_tree_view.css",__file__)

class tree_view(uix.Element):
    def __init__(self, id=None, data=None, callback=None, selected_label=None, default_open=True):
        super().__init__(id=id)
        self.data = data or {}
        self.callback = callback
        self.selected_label = selected_label

        with self:
            with unorderedlist().cls("tree"):
                for main_title, items in self.data.items():
                    self.create_tree(main_title, items, default_open and list(self.data.keys())[0])  

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