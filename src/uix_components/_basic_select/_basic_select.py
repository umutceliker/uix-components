from uix.elements import select, option

class basic_select(select):
    def __init__(
            self,
            id=None,
            value=None,
            options : dict[str, str] = None,
            callback=None,
            **kwargs
        ):
        super().__init__( id=id, **kwargs)
        self.options = options
        self.callback = callback

        with self.on("change", self.on_change):    
            if type(self.options) == list:
                for _option in self.options:
                    if _option["isSelect"] == True:
                        option(id=_option['id'], value=_option['id'], text=_option['value']).selected()
                    else:
                        option(id=_option['id'], value=_option['id'], text=_option['value'])
            else:
                for key, value in self.options.items():
                    if value["isSelect"] == True:
                        option(value=key, id=value["id"], text=value["value"]).selected()
                    else:
                        option(value=key, id=value["id"], text=value["value"])

    def on_change(self, ctx, id, value):
        self.value = value
        if self.callback:
            self.callback(ctx, id, value)

title = "Basic Select"
description = """
# basic_select(id, value, options callback)
1. Basic Select bir select komponentidir.
    | attr          | desc                                                       |
    | :------------ | :-----------------------------------------------------     |
    | id            | Komponentin id'si                                          |
    | value         | Komponentin değeri                                         |
    | options       | Komponentin seçenekleri dict veya list olarak verilebilir. |
    | callback      | Komponentin değeri değiştiğinde çalışacak fonksiyon        |
"""
sample="""
from uix.elements import text
from uix_components import basic_select

options = [
    {"id":"1","isSelect":False, "value":"Option 1"},
    {"id":"2","isSelect":False, "value":"Option 2"},
    {"id":"3","isSelect":True, "value":"Option 3"},
]

def on_change(ctx,id,value):
    ctx.elements["test"].value = value
    ctx.elements["test"].update()

def basic_select_example():
    basic_select(id = "mySelect",options = options, callback=on_change)
    text(id="test", value="Select Value")
"""