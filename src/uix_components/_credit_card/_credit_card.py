import os
import io
import uix
from uix.elements import row

uix.html.add_css_file("_credit_card.css",__file__)
uix.html.add_script_source(id="credit_card",script="imask.min.js",beforeMain=False,localpath=__file__)
uix.html.add_script_source(id="credit_card_ui",script="_credit_card.js",beforeMain=False,localpath=__file__)
uix.html.add_script_source(id="credit_card",script="_add_card.js",beforeMain=False,localpath=__file__)


path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "_credit_card")
uix.app.add_static_route("credit_card",path)

with io.open(os.path.join(path,"_credit_card.html"), mode="r", encoding="utf-8") as f:
     html_content=f.read()
     f.close

class credit_card(uix.Element):
    def __init__(self, value, id = None):
            super().__init__(value,id = id)
            self.path=path
            self.size("100%","100%")
            print("credit_card init")
            with self:
                with row("",id="credit-cards").cls("credit-card-row") as creditcard:
                    self.creditcard=creditcard
                
    def init(self):
        print("credit_card init")
        self.session.queue_for_send(self.id,{
            'creditcard': self.creditcard.id,
            'html_content': html_content,
            }, 

             "init-credit-card")
                
                
title = "Credit Card"
description = """
## credit_card(value, id = None)

1- Kredi kartı bilgilerinin girilebileceği bir alan oluşturur.

| attr                  | desc                                              |
| :-------------------- | :------------------------------------------------ |
| id                    | credit_card elementinin id'si                         |

"""

sample="""
    def credit_card_example():
        with div("").size("60%","50%") as credit_card_example:
            credit_card("",id="credit_card_example")
        return credit_card_example 
    """

