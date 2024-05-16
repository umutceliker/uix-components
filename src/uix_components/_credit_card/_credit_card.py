import os
import io
import uix
from uix import T
from uix.elements import row,button,div

uix.html.add_css_file("_credit_card.css",__file__)
uix.html.add_script_source(id="credit_card",script="imask.min.js",beforeMain=False,localpath=__file__)
uix.html.add_script_source(id="credit_card_ui",script="_credit_card.js",beforeMain=False,localpath=__file__)
uix.html.add_script_source(id="add_card_js",script="_add_card.js",beforeMain=False,localpath=__file__)


path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "_credit_card")
uix.app.add_static_route("credit_card",path)

with io.open(os.path.join(path,"_credit_card.html"), mode="r", encoding="utf-8") as f:
                html_content=f.read()
                f.close

class credit_card(uix.Element):
    def __init__(self, value, id = None, callback=None):
            super().__init__(value,id = id)
            self.path=path
            self.callback=callback
            self.size("100%","100%")
            self.html_content=html_content
            with self:
                with row("",id="credit-cards").cls("credit-card-row") as creditcard:
                    self.creditcard=creditcard
                    with div(id="add_card_div").cls("field-container") as add_card_div:
                        self.add_card_div=add_card_div
                        button(T("Add Card"),id="payment-button",type="submit").cls("payment-button").on("add_card", self.callback)
                
    def init(self):
        self.session.queue_for_send(self.id,{
            'creditcard': self.creditcard.id,
            'html_content': self.html_content,
            'add_card_div': self.add_card_div.id
            }, 

             "init-credit-card")

