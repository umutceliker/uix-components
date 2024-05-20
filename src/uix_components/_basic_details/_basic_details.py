import uix
from uix.elements import details, text, div

uix.html.add_css_file("_basic_details.css",__file__)
class basic_details(uix.Element):
    def __init__(self, value, id = None,label_=None, acc_elements = list()):
        super().__init__(value,id = id)
        self.cls("border")
        self.style("width","100%")
        with self:
            with details(id=id+"-details").cls("default square"):
                text(label_).tag="summary"
                if acc_elements:
                    for element in acc_elements:
                        with div().cls("details_acc"):
                            element()
