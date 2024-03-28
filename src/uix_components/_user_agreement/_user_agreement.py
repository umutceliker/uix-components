import os
import io
import uix
from uix.elements import row, col, button

uix.html.add_css_file("_user_agreement.css",__file__)
uix.html.add_script_source(id="useragreement-js",script="_user_agreement.js",beforeMain=False,localpath=__file__)

path=os.path.join(os.path.dirname(os.path.dirname(__file__)), "_user_agreement")

class user_agreement(uix.Element):
    def __init__(self,
                id=None,
                user_agreement=None,
                func_name=None,
                **kwargs
                ):
        super().__init__(id=id)
        self.id=id
        self.accept=False
        self.func_name=func_name
        self.user_agreement=user_agreement
        with self as content:
            self.content=content
            with col("").cls("userAgreement"):
                self.contract=row("",id="contract")
                with row("").cls("term-buttons-container"):
                    self.accept_btn=button(value="Kabul Et",id=id+"-accept-btn").cls("accept-button hidden")

    def init(self):
        self.session.queue_for_send(
            self.id,
            {
                "id": self.id,
                "contract": self.contract.id,
                "contract_content": self.user_agreement,
                "accept_btn": self.accept_btn.id,
                "accept": self.accept,
                "func_name": self.func_name
            },
        "init-contract"),
        return super().render()
