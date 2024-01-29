import uix
import os
from uix.elements import details, text, div, check,label,button

uix.html.add_css_file("_basic_details.css",__file__)
class basic_details(uix.Element):
    def __init__(self, value, id = None,label_=None, acc_elements = list()):
        super().__init__(value,id = id)
        self.cls("border")
        self.style("width","100%")
        with self:
            with details().cls("default square"):
                text(label_).tag="summary"
                if acc_elements:
                    for element in acc_elements:
                        with div().cls("details_acc"):
                            element()
        

title = "Basic Details"
"""# dialog(value,id = None, is_clickable_anywhere = True)

1. Dialog elementi. Bir dialog penceresi açar.

| attr                  | desc                                              |
| :-------------------- | :------------------------------------------------ |
| id                    | Dialog elementinin id'si                          |
| value                 | Dialog elementinin içeriği                       |
| close_on_outside      | Dışarı tıklanınca kapanma özelliği               |"""
description = """  
# basic_details("",id = "myDetails",label_="Accordion Example", acc_elements = [acc_elements_example] )

1- Bilgilerin yalnızca widget "açık" duruma getirildiğinde görülebildiği bir açıklama widget'ı oluşturur.

| attr                  | desc                                              |
| :-------------------- | :------------------------------------------------ |
| id                    | Details elementinin id'si                         |
| label_                | Details elementinin başlığı                       |
| acc_elements          | Details elementinin içeriği, bir liste olmalıdır  |"""

sample="""
        def acc_elements_example():
            with col() as col1:
                col1.cls("border")
                basic_slider(name="Deneme1", id = "mySlider1", callback = lambda ctx, id, value: print(f"Slider {id} changed to: {value}"))
                basic_slider(name="Deneme2", id = "mySlider2",callback=lambda ctx, id, value: print(f"Slider {id} changed to: {value}"))
                basic_slider(name="Deneme3", id = "mySlider3",callback=lambda ctx, id, value: print(f"Slider {id} changed to: {value}"))
                button("Button 1")
        def basic_details_example():
            with div() as details:
                details.size("50%","max-content")
                basic_details("",id = "myDetails",label_="Accordion Example", acc_elements = [acc_elements_example] )
            return details     
"""
